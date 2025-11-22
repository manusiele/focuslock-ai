# FocusLock AI Agent

Your personal AI co-pilot that logs your Termux activity (clones, commands, apps) and suggests hyper-personalized tech projects via Telegram. Runs offline on Android with Phi-3 Mini.

## Quick Termux Install
```bash
pkg update -y && pkg install git python ffmpeg termux-api ollama -y
pip install chromadb python-telegram-bot requests sentence-transformers torch
git clone https://github.com/manusiele/focuslock-ai.git ~/focuslock-ai
cd ~/focuslock-ai
cp .env.example .env  # Edit with your BOT_TOKEN
ollama pull phi3:mini  # ~2GB, one-time
python focuslock.py --daemon  # Starts logging + bot
