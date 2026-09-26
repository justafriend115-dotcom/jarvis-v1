# main.py
import threading
import queue
import time
import re
from brain import think
from tools import AVAILABLE_TOOLS, get_system_stats
from council import council
import voice
from gui import ZeusGUI
import customtkinter as ctk

def brain_worker(process_queue, response_queue):
    """Background thread that handles the AI logic so the GUI doesn't freeze."""
    WAKE_WORD = "zeus"

    while True:
        # 1. Handle inputs from the GUI
        try:
            user_input = process_queue.get(timeout=0.1)
            # Process GUI input directly
            response = handle_logic(user_input, response_queue)
        except queue.Empty:
            # 2. Handle Voice Input (Passive Listening)
            voice_input = voice.listen()
            if voice_input:
                # Only process if wake word is present
                if WAKE_WORD in voice_input.lower():
                    clean_input = voice_input.lower().replace(WAKE_WORD, "").strip()
                    if not clean_input:
                        response_queue.put(("text", "Yes, sir? I am listening."))
                        voice.speak("Yes, sir? I am listening.")
                        # Listen again for the actual command
                        clean_input = voice.listen()
                        if not clean_input: continue
                        clean_input = clean_input.lower().replace(WAKE_WORD, "").strip()

                    response = handle_logic(clean_input, response_queue)
                else:
                    # Quietly log passive input to the GUI
                    response_queue.put(("status", f"Passive: {voice_input}"))
            else:
                # Just a heartbeat for stats
                stats = get_system_stats().replace("CPU Usage: ", "").replace(" | RAM Usage: ", "").split("%")
                try:
                    cpu = stats[0].strip()
                    ram = stats[1].strip("%")
                    response_queue.put(("stats", (cpu, ram)))
                except: pass

def handle_logic(user_input, response_queue):
    if "go offline" in user_input or "shutdown" in user_input:
        response_queue.put(("text", "Shutting down systems. Goodbye, sir."))
        voice.speak("Shutting down systems. Goodbye, sir.")
        # In a real app, we'd trigger a window close here
        return

    response_queue.put(("status", f"Processing: {user_input}..."))
    response_queue.put(("core", "#FFD700")) # Turn Gold while thinking

    response = think(user_input)

    match = re.search(r"TOOL:\s*(\w+)\((.*)\)", response)
    if match:
        tool_name = match.group(1)
        arg_string = match.group(2)

        if tool_name == "convene_council":
            response_queue.put(("status", "Convening the Council of Olympus..."))
            result = council.convene(arg_string.strip('"').strip("'"))
            response_queue.put(("text", result))
            voice.speak(result)
        elif tool_name in AVAILABLE_TOOLS:
            response_queue.put(("status", f"Executing {tool_name}..."))
            func = AVAILABLE_TOOLS[tool_name]
            try:
                if arg_string.strip():
                    args = [a.strip().strip('"').strip("'") for a in arg_string.split(',')]
                else:
                    args = []
                result = func(*args)
                response_queue.put(("text", result))
                voice.speak(result)
            except Exception as e:
                err = f"Error executing {tool_name}: {e}"
                response_queue.put(("text", err))
                voice.speak(err)
        else:
            response_queue.put(("text", "Tool not found."))
            voice.speak("Tool not found.")
    else:
        response_queue.put(("text", response))
        voice.speak(response)

    response_queue.put(("core", "#00BFFF")) # Return to Blue

if __name__ == "__main__":
    # Queues for communication between GUI and Brain
    process_q = queue.Queue()
    response_q = queue.Queue()

    # Start the Brain in a background thread
    brain_thread = threading.Thread(target=brain_worker, args=(process_q, response_q), daemon=True)
    brain_thread.start()

    # Start the GUI in the main thread
    app = ZeusGUI(process_q, response_q)
    app.mainloop()
