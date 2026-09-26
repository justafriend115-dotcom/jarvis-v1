# tools.py
import os
import subprocess
import psutil
import webbrowser
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from duckduckgo_search import DDGS
from requests.auth import HTTPBasicAuth

MEMORY_FILE = "memory.json"
LAST_CALL_FILE = "last_call.json"

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

def web_search(query):
    """Searches the web for snippets of information."""
    print(f"[*] Zeus is searching the web for: {query}...")
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            if not results:
                return "I found no results on the web, sir."
            return "\n\n".join(results)
    except Exception as e:
        return f"The web search failed: {str(e)}"

def deep_research(query):
    """Performs a comprehensive deep-dive into a topic."""
    print(f"[*] Zeus is initiating a deep research dive into: {query}...")
    try:
        with DDGS() as ddgs:
            search_results = list(ddgs.text(query, max_results=3))
            if not search_results:
                return "I found no sources for this deep dive, sir."
            all_content = []
            for result in search_results:
                url = result['href']
                try:
                    response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        for script_or_style in soup(["script", "style", "header", "footer", "nav"]):
                            script_or_style.decompose()
                        text = soup.get_text(separator=' ')
                        lines = (line.strip() for line in text.splitlines())
                        chunks = (phrase.strip() for phrase in lines for phrase in phrase.split('\n'))
                        cleaned_text = '\n'.join(chunk for chunk in chunks if chunk)
                        all_content.append(f"Source: {url}\nContent: {cleaned_text[:3000]}")
                except Exception: continue
            if not all_content: return "I couldn't extract content from any sources."
            return "\n\n---\n\n".join(all_content)
    except Exception as e:
        return f"Deep research failed: {str(e)}"

def make_emergency_call(message):
    """Triggers a real phone call via Twilio REST API."""
    import os
    # Load credentials from .env
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")
    to_number = os.getenv("MY_PHONE_NUMBER")

    if not all([account_sid, auth_token, from_number, to_number]):
        return "Emergency system failure: Twilio credentials are missing from .env"

    # Cool-down timer: Prevent spamming (15 minutes)
    now = datetime.now().timestamp()
    if os.path.exists(LAST_CALL_FILE):
        with open(LAST_CALL_FILE, "r") as f:
            try:
                last_call = float(f.read())
                if now - last_call < 900: # 900 seconds = 15 mins
                    return "I attempted a call recently. I cannot call again for another 15 minutes to avoid spamming you, sir."
            except: pass

    # Twilio API Endpoint for Calls
    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Calls.json"

    # TwiML: The instructions for what the voice should say on the phone
    twiml_content = f"<Response><Say voice='alice'>{message}</Say></Response>"

    data = {
        "To": to_number,
        "From": from_number,
        "Twiml": twiml_content
    }

    try:
        response = requests.post(url, data=data, auth=HTTPBasicAuth(account_sid, auth_token))
        if response.status_code == 201:
            with open(LAST_CALL_FILE, "w") as f:
                f.write(str(now))
            return "Emergency call initiated. Your phone should ring momentarily, sir."
        else:
            return f"Twilio API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Physical connection failed: {str(e)}"

AVAILABLE_TOOLS = {
    "get_time": get_time,
    "get_system_stats": get_system_stats,
    "open_website": open_website,
    "open_app": open_app,
    "save_memory": save_memory,
    "get_memory": get_memory,
    "web_search": web_search,
    "deep_research": deep_research,
    "make_emergency_call": make_emergency_call # New!
}
