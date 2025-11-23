import os
import json
from datetime import datetime
import requests
import ollama
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MODEL = "phi3:mini"

# Simple persistent history
os.makedirs("data", exist_ok=True)
HISTORY_FILE = "data/history.json"

if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
else:
    history = [
        "Building real apps from PC only — no Termux ever",
        "Obsessed with clean deploys: Vercel, Railway, Render, Fly.io",
        "Wants project name + exact stack + useful links only"
    ]

def log_activity(text: str):
    entry = f"{text} — {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    history.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def get_context() -> str:
    return "\n".join(history[-7:]) if history else "Fresh PC warrior."

def generate_idea() -> str:
    context = get_context()
    prompt = f"""You are FocusLock — elite, no-BS AI co-pilot for a Kenyan dev building from PC only.

Recent vibe:
{context}

Give exactly ONE real-world project that:
• Is built and deployed from Windows/Linux/macOS laptop
• Goes live on Vercel, Render, Railway, Fly.io, Northflank, etc.
• Can be shipped in one focused session (2–8 hours)
• Has actual money or portfolio value

Format ONLY (no extra words, no commands):
Project → [badass name]
Stack → [exact tools + frameworks]
Deploy → [one platform]
Docs & Links →
• [name] → [url]
• [name] → [url]
• [name] → [url]
Why now → [1 savage sentence]
Potential → [real KSh, users, gigs, stars]"""

    response = ollama.generate(model=MODEL, prompt=prompt)
    return response["response"]

def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown", "disable_web_page_preview": True}
    try:
        requests.post(url, data=payload, timeout=10)
        print("Ping sent")
    except Exception as e:
        print(f"Telegram failed: {e}")

if __name__ == "__main__":
    idea = generate_idea()
    message = f"*FocusLock • PC Edition*\n{datetime.now().strftime('%b %d • %H:%M')} EAT\n\n{idea}"
    send_telegram(message)
    log_activity("Delivered clean project idea (no commands, links only)")
