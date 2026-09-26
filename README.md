# 🤖 JARVIS v1 - Autonomous OS Assistant

Jarvis v1 is a tool-enabled AI agent designed to bridge the gap between Large Language Models (LLMs) and local system operations. Instead of just chatting, Jarvis can reason about a user's intent and execute real-world actions on a Windows machine.

## ✨ Features
- **🧠 Brain:** Powered by the `Llama-3` model via **Groq Cloud API** for near-instant response times.
- **🛠️ Tool-Use Architecture:** Implements a custom function-calling loop that allows the AI to trigger Python functions based on natural language.
- **💾 Long-Term Memory:** A persistent JSON-based memory system that allows Jarvis to remember user preferences and personal facts across sessions.
- **🖥️ System Integration:**
    - Control applications (Notepad, Calculator, etc.)
    - Web automation (Opening specific URLs)
    - System monitoring (CPU/RAM usage and system time)

## 🚀 Tech Stack
- **Language:** Python 3.11
- **LLM Provider:** Groq (Llama-3)
- **Key Libraries:** `groq`, `psutil`, `python-dotenv`

## 🛠️ Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/jarvis-v1.git
   cd jarvis-v1
2. Install dependencies:
pip install -r requirements.txt
3. Create a .env file in the root directory and add your API key:
GROQ_API_KEY=your_api_key_here
4. Run the assistant:
python main.py

📈 Future Roadmap

- [ ] Voice Integration: Adding Speech-to-Text (STT) and Text-to-Speech (TTS).
- [ ] Vision: Implementing screenshot analysis using Multimodal LLMs.
- [ ] Advanced Automation: Email and Calendar integration.
