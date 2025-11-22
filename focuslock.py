import os
import json
from datetime import datetime
import requests
import ollama
from chromadb import PersistentClient
from chromadb.utils import embedding_functions
from dotenv import load_dotenv  # For local testing, optional

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
MODEL = 'phi3:mini'

# Persistent DB setup (saves to ./data/)
os.makedirs('data', exist_ok=True)
client = PersistentClient(path='./data')
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_or_create_collection(name="activity", embedding_function=ef)

# Load history JSON (for quick access)
HISTORY_FILE = 'data/history.json'
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)
else:
    history = []

def log_activity(text):
    timestamp = datetime.now().isoformat()
    doc = f"{text} at {timestamp}"
    history.append(doc)
    
    # Embed to Chroma
    collection.add(documents=[doc], ids=[str(len(history))])
    
    # Save JSON
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)
    print(f"Logged: {doc}")

def get_context():
    if len(history) == 0:
        return "No activity yet—start by logging something!"
    results = collection.query(query_texts=["recent tech activity"], n_results=5)
    return '\n'.join(results['documents'][0]) if results['documents'] else '\n'.join(history[-5:])

def generate_idea():
    context = get_context()
    prompt = f"""You are FocusLock: no-BS AI for a Kenyan CS student building in cloud/Termux.
User history: {context}

Suggest ONE buildable project (100-300 lines, Python/JS focus):
- Ties to history (e.g., if cloning AI repos, suggest fine-tune).
- Levels up skills: AI, web3, M-Pesa hacks, chaos tools.
- Real value: KSh hustle, portfolio, or fun exploit.
- Format:
Project: [Name]
Why: [1 sentence]
Stack: [pkg/tools]
Steps: 1. [cmd] 2. [cmd]
Time: 2-4h
Potential: [outcome]"""
    
    response = ollama.generate(model=MODEL, prompt=prompt)
    return response['response']

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
    requests.post(url, data=data)
    print("Sent to Telegram")

if __name__ == "__main__":
    # Default: Generate and send idea
    idea = generate_idea()
    message = f"🔒 *FocusLock Ping*\n\n{idea}"
    send_telegram(message)
