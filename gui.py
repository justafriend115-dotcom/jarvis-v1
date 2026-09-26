# gui.py
import customtkinter as ctk
import threading
import queue

class ZeusGUI(ctk.CTk):
    def __init__(self, process_queue, response_queue):
        super().__init__()

        # Window Configuration
        self.title("ZEUS OS - Command Center")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.process_queue = process_queue
        self.response_queue = response_queue

        # Animation state
        self.pulse_state = False
        self.pulse_size = 80
        self.base_size = 80

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- LEFT SIDEBAR (System Stats) ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.logo_label = ctk.CTkLabel(self.sidebar, text="ZEUS", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.pack(pady=20)

        self.stats_label = ctk.CTkLabel(self.sidebar, text="System: Online", font=ctk.CTkFont(size=12))
        self.stats_label.pack(pady=10)

        self.cpu_label = ctk.CTkLabel(self.sidebar, text="CPU: --%", font=ctk.CTkFont(size=12))
        self.cpu_label.pack(pady=5)

        self.ram_label = ctk.CTkLabel(self.sidebar, text="RAM: --%", font=ctk.CTkFont(size=12))
        self.ram_label.pack(pady=5)

        self.clear_btn = ctk.CTkButton(self.sidebar, text="Clear Log", command=self.clear_log, fg_color="#333333", hover_color="#444444")
        self.clear_btn.pack(side="bottom", pady=20)

        # --- MAIN AREA ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # The "Core" (Visual Indicator)
        self.core_canvas = ctk.CTkLabel(
            self.main_container,
            text="⚡",
            font=ctk.CTkFont(size=self.base_size),
            text_color="#00BFFF"
        )
        self.core_canvas.grid(row=0, column=0, pady=(20, 10))

        # The Log (Conversation History)
        self.log_box = ctk.CTkTextbox(self.main_container, width=600, height=300, font=ctk.CTkFont(size=13))
        self.log_box.grid(row=1, column=0, sticky="nsew", pady=10)
        self.log_box.configure(state="disabled")

        # Input Area
        self.input_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, sticky="ew", pady=10)
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter command or say 'Zeus'...", height=40)
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.entry.bind("<Return>", lambda event: self.send_message())

        self.send_btn = ctk.CTkButton(self.input_frame, text="Send", width=100, command=self.send_message)
        self.send_btn.grid(row=0, column=1)

        # Start the polling threads
        self.after(100, self.poll_responses)
        self.after(100, self.pulse_animation)

    def send_message(self):
        msg = self.entry.get()
        if msg:
            self.log_message(f"You: {msg}")
            self.process_queue.put(msg)
            self.entry.delete(0, 'end')

    def log_message(self, text):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.configure(state="disabled")
        self.log_box.see("end")

    def clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

    def update_stats(self, cpu, ram):
        self.cpu_label.configure(text=f"CPU: {cpu}%")
        self.ram_label.configure(text=f"RAM: {ram}%")

    def set_core_color(self, color):
        self.core_canvas.configure(text_color=color)

    def pulse_animation(self):
        """Smoothly animates the core size to create a pulsing effect."""
        if self.pulse_state:
            self.pulse_size -= 1
            if self.pulse_size <= 70:
                self.pulse_state = False
        else:
            self.pulse_size += 1
            if self.pulse_size >= 90:
                self.pulse_state = True

        self.core_canvas.configure(font=ctk.CTkFont(size=self.pulse_size))
        self.after(50, self.pulse_animation)

    def poll_responses(self):
        try:
            while not self.response_queue.empty():
                msg_type, content = self.response_queue.get_nowait()
                if msg_type == "text":
                    self.log_message(f"Zeus: {content}")
                elif msg_type == "status":
                    self.log_message(f"[*] {content}")
                elif msg_type == "stats":
                    cpu, ram = content
                    self.update_stats(cpu, ram)
                elif msg_type == "core":
                    self.set_core_color(content)
        except queue.Empty:
            pass
        self.after(100, self.poll_responses)
