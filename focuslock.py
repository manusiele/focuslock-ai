import os
import json
from datetime import datetime
import requests
import ollama
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MODEL = "phi3:mini"  # or "llama3.2", "gemma2", etc.

# Persistent history
os.makedirs("data", exist_ok=True)
HISTORY_FILE = "data/history.json"

if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
else:
    history = [
        "Building real apps from PC only — no Termux ever",
        "Obsessed with clean deploys: Vercel, Railway, Render, Fly.io",
        "Wants project name + exact stack + useful links only",
        "Every idea must start with a sharp Problem Statement"
    ]

def log_activity(text: str):
    entry = f"{text} — {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    history.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def get_context() -> str:
    return "\n".join(history[-8:]) if history else "Fresh PC warrior."

def generate_idea() -> str:
    context = get_context()
    prompt = f"""You are FocusLock — elite, no-fluff AI co-pilot for a Kenyan dev building real apps from PC only.

Recent vibe:
{context}

Generate exactly ONE focused project idea with this EXACT format (no extra text, no greetings):

PROBLEM STATEMENT
Who → [People trying to build or grow modern businesses across Africa. This includes agritech innovators, agrotech startups, smallholder-focused platforms, fintech creators, digital freelancers, junior developers, micro-SME owners, content creators, e-commerce sellers, and tech-curious youth stepping into the digital economy. ]
Pain → [They wrestle with scattered information, outdated tools, slow manual workflows, limited market access, unreliable data, and lack of affordable digital support. Every task feels like pushing a heavy cart through wet soil: slow, repetitive, and draining. Most spend hours figuring out what should take minutes.]
Gap → [There’s no unified, affordable, intelligent system that simplifies their operations, automates routine tasks, gives reliable insights, and supports growth across sectors. Existing solutions are either too expensive, too generic, too technical, or not built for the African business environment.]
Impact if unsolved → [They lose money through inefficiency, waste time that could grow their business, miss opportunities due to poor data, struggle to scale, and remain stuck in survival mode instead of growth mode. Careers stall, businesses plateau, and innovation slows]

Project → [badass, memorable name]
Stack → [exact tools only, e.g. Next.js + Supabase + Vercel]
Deploy → [one platform: Vercel / Railway / Render / Fly.io / Northflank]
Docs & Links →
• [Tool] → [url]
• [Tool] → [url]
• [Tool] → [url]
Why now → [one brutal truth sentence]
Potential → [realistic KSh, users, gigs, GitHub stars, or portfolio power]"""

    response = ollama.generate(model=MODEL, prompt=prompt)
    return response["response"]

def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        resp = requests.post(url, data=payload, timeout=15)
        if resp.status_code == 200:
            print("✅ Ping sent to Telegram")
        else:
            print(f"⚠️ Telegram returned {resp.status_code}: {resp.text}")
    except requests.exceptions.Timeout:
        print("❌ Telegram timeout after 15s")
    except Exception as e:
        print(f"❌ Telegram failed: {e}")

if __name__ == "__main__":
    try:
        print("🔥 FocusLock starting...")
        idea = generate_idea()
        timestamp = datetime.now().strftime('%b %d • %H:%M') 
        message = f"*FocusLock • PC Edition*\n{timestamp} EAT\n\n{idea}"
        
        send_telegram(message)
        log_activity("Delivered project with Problem Statement + clean stack")
        print("✅ FocusLock complete")
    except Exception as e:
        print(f"❌ FocusLock crashed: {e}")
        raise
