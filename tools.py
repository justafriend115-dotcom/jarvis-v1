# tools.py
import os
import subprocess
import psutil
import webbrowser
import json
from datetime import datetime

MEMORY_FILE = "memory.json"

def load_memory():
    """Helper function to load memory from the JSON file."""
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {}

def save_memory(key, value):
    """Saves a piece of information to long-term memory."""
    memory = load_memory()
    memory[key] = value
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)
    return f"I've remembered that {key} is {value}, sir."

def get_memory(key):
    """Retrieves a piece of information from long-term memory."""
    memory = load_memory()
    return memory.get(key, "I don't have any record of that in my database, sir.")

def get_time():
    """Returns the current system time."""
    return datetime.now().strftime("%H:%M:%S")

def get_system_stats():
    """Returns CPU and RAM usage."""
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    return f"CPU Usage: {cpu}% | RAM Usage: {ram}%"

def open_website(url):
    """Opens a website in the default browser."""
    webbrowser.open(url)
    return f"Opened {url} in your browser."

def open_app(app_name):
    """Attempts to open a Windows application."""
    try:
        subprocess.Popen(f"start {app_name}", shell=True)
        return f"Attempting to open {app_name}..."
    except Exception as e:
        return f"Failed to open {app_name}: {str(e)}"

# Updated mapping to include memory tools
AVAILABLE_TOOLS = {
    "get_time": get_time,
    "get_system_stats": get_system_stats,
    "open_website": open_website,
    "open_app": open_app,
    "save_memory": save_memory, # New!
    "get_memory": get_memory    # New!
}