import os
import json
from datetime import datetime
import requests
import ollama
from dotenv import load_dotenv
import random

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

# Universal problem domains
PROBLEM_DOMAINS = [
    {
        "who": "Small business owners, freelancers, and solopreneurs trying to grow their ventures",
        "pain": "They juggle invoicing, client communication, bookkeeping, and marketing manually across scattered tools. Every task eats hours that could be spent on actual work. Cash flow tracking is a nightmare, client follow-ups get missed, and tax season becomes panic mode.",
        "gap": "There's no affordable, unified system that handles money management, client relations, and business operations in one place without requiring accounting degrees or expensive subscriptions.",
        "impact": "They lose revenue through poor cash flow visibility, waste 10+ hours weekly on admin tasks, miss growth opportunities due to disorganization, and risk business failure from financial mismanagement."
    },
    {
        "who": "Students, job seekers, and career switchers trying to break into tech or advance their skills",
        "pain": "They're overwhelmed by scattered learning resources, unclear career paths, and the gap between online courses and real-world skills. Building portfolios feels impossible without guidance, and job applications disappear into black holes.",
        "gap": "There's no personalized learning system that combines skill tracking, project guidance, portfolio building, and job matching based on actual capabilities and market demand.",
        "impact": "They waste months learning irrelevant skills, struggle to prove competence to employers, miss job opportunities due to poor portfolio presentation, and remain stuck in low-paying roles."
    },
    {
        "who": "Content creators, influencers, and digital entrepreneurs building online presence",
        "pain": "They struggle to maintain consistent posting schedules, analyze what content works, manage multiple platforms, and turn engagement into revenue. Content ideas dry up, analytics are confusing, and monetization feels like guesswork.",
        "gap": "There's no intelligent system that generates content ideas based on trends, optimizes posting schedules, tracks cross-platform performance, and recommends monetization strategies.",
        "impact": "They lose followers due to inconsistent posting, waste effort on low-performing content, miss viral opportunities, and struggle to convert audience into sustainable income."
    },
    {
        "who": "Remote teams, distributed startups, and async-first companies trying to stay aligned",
        "pain": "They drown in endless Slack messages, meetings that could be emails, scattered documentation, and timezone chaos. Important decisions get lost in chat history, onboarding new members takes weeks, and project context evaporates.",
        "gap": "There's no async-first platform that captures decisions, maintains living documentation, surfaces relevant context automatically, and keeps everyone aligned without synchronous meetings.",
        "impact": "They waste hours in unnecessary meetings, duplicate work due to poor knowledge sharing, struggle with employee retention, and move too slowly to compete with faster teams."
    },
    {
        "who": "Health-conscious individuals trying to improve fitness, nutrition, and mental wellbeing",
        "pain": "They're lost in conflicting diet advice, can't stick to workout plans, track progress inconsistently, and ignore mental health until crisis hits. Generic apps don't adapt to their lifestyle, and personal trainers are too expensive.",
        "gap": "There's no adaptive wellness system that combines personalized nutrition, progressive fitness plans, mental health check-ins, and habit formation based on individual goals and constraints.",
        "impact": "They waste money on ineffective programs, yo-yo between fitness phases, develop health problems from neglect, and feel constant guilt about unmet wellness goals."
    },
    {
        "who": "Parents managing family schedules, finances, and children's development",
        "pain": "They coordinate school activities, medical appointments, meal planning, and budgets across multiple apps while trying to track kids' academic progress and emotional wellbeing. Everything feels urgent and nothing gets the attention it deserves.",
        "gap": "There's no family operating system that centralizes schedules, automates routine planning, tracks child development milestones, and provides gentle reminders for important tasks.",
        "impact": "They miss important appointments, feel constantly overwhelmed, struggle with work-life balance, and worry they're failing their children due to disorganization."
    },
    {
        "who": "Local service providers (plumbers, electricians, tutors, cleaners) trying to find and retain clients",
        "pain": "They rely on word-of-mouth, struggle with online visibility, lack professional booking systems, and lose clients to more tech-savvy competitors. Marketing feels too expensive and complicated.",
        "gap": "There's no local services platform that handles discovery, booking, payments, and review management specifically designed for service professionals without technical skills.",
        "impact": "They remain dependent on expensive middleman platforms, struggle with irregular income, miss potential clients, and can't scale beyond their immediate network."
    },
    {
        "who": "Researchers, writers, and knowledge workers managing information overload",
        "pain": "They save articles, papers, and notes across browsers, apps, and devices but can never find them when needed. Connecting ideas is manual, citations are a nightmare, and synthesizing research takes forever.",
        "gap": "There's no intelligent knowledge management system that automatically organizes sources, surfaces connections, generates summaries, and helps transform research into original writing.",
        "impact": "They waste hours re-finding information, struggle with writer's block, miss important connections between ideas, and produce lower-quality work than their research deserves."
    },
    {
        "who": "E-commerce sellers managing inventory, orders, and customer service across platforms",
        "pain": "They manually track stock across marketplaces, respond to customer queries on multiple channels, struggle with shipping logistics, and have no clear view of profitability per product.",
        "gap": "There's no unified commerce dashboard that syncs inventory in real-time, centralizes customer communication, automates routine responses, and provides clear profit analytics.",
        "impact": "They oversell products causing customer complaints, waste hours on repetitive messages, lose money on unprofitable items, and can't scale without hiring expensive help."
    },
    {
        "who": "Event organizers managing registrations, communications, and logistics for gatherings",
        "pain": "They cobble together registration forms, email lists, payment collection, and attendee communication using disconnected tools. Last-minute changes become nightmares, and attendee engagement drops off after registration.",
        "gap": "There's no end-to-end event platform that handles registration, automated reminders, attendee networking, real-time updates, and post-event follow-up in one place.",
        "impact": "They lose attendees to poor communication, struggle with low engagement, waste hours on manual coordination, and can't build community beyond single events."
    },
    {
        "who": "Nonprofit organizations trying to manage donors, volunteers, and impact tracking",
        "pain": "They manually track donations in spreadsheets, struggle to engage volunteers consistently, can't demonstrate impact to funders, and spend too much time on admin instead of mission work.",
        "gap": "There's no affordable nonprofit management system that combines donor CRM, volunteer coordination, impact measurement, and automated reporting for grant applications.",
        "impact": "They lose donors due to poor engagement, struggle to secure funding without clear impact data, burn out volunteers with disorganization, and ultimately serve fewer people."
    },
    {
        "who": "Landlords and property managers handling multiple rental properties",
        "pain": "They manually track rent payments, maintenance requests pile up in texts and emails, tenant screening is time-consuming, and financial reporting for taxes is a mess.",
        "gap": "There's no simple property management system that automates rent collection, centralizes maintenance tracking, screens tenants, and generates financial reports automatically.",
        "impact": "They lose income from missed payments, face tenant complaints due to slow maintenance, make bad tenant choices, and panic during tax season with incomplete records."
    },
    {
        "who": "Personal finance enthusiasts trying to achieve financial independence and smart investing",
        "pain": "They track expenses manually, can't visualize long-term financial goals, struggle to optimize investments across accounts, and miss tax-saving opportunities due to complexity.",
        "gap": "There's no holistic financial dashboard that aggregates all accounts, projects retirement scenarios, recommends optimizations, and identifies tax strategies automatically.",
        "impact": "They miss wealth-building opportunities, pay unnecessary taxes, feel anxious about retirement readiness, and make suboptimal financial decisions from incomplete information."
    },
    {
        "who": "Agritech innovators, smallholder farmers, and agrotech startups trying to modernize agriculture",
        "pain": "They wrestle with unpredictable weather, market price volatility, limited access to quality inputs, poor supply chain visibility, and lack of data to make informed planting decisions.",
        "gap": "There's no integrated platform that combines weather forecasts, market prices, input sourcing, farm management, and direct buyer connections for small-scale farmers.",
        "impact": "They lose entire harvests to preventable issues, sell crops below market rate, struggle with food security, and remain trapped in subsistence farming instead of profitable agribusiness."
    },
    {
        "who": "Mental health professionals managing clients, notes, billing, and compliance",
        "pain": "They juggle HIPAA-compliant note-taking, appointment scheduling, insurance billing, and client progress tracking across multiple systems while trying to provide quality care.",
        "gap": "There's no affordable, compliant practice management system designed specifically for solo therapists and small mental health practices that handles all aspects of practice management.",
        "impact": "They waste therapy time on admin work, risk compliance violations, lose revenue to billing errors, and burn out trying to manage business operations alongside clinical work."
    }
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
    
    # Select random problem domain
    problem = random.choice(PROBLEM_DOMAINS)
    
    prompt = f"""You are FocusLock — elite, no-fluff AI co-pilot for a developer building real apps from PC only.

Recent vibe:
{context}

Generate exactly ONE focused project idea with this EXACT format (no extra text, no greetings):

PROBLEM STATEMENT
Who → {problem['who']}
Pain → {problem['pain']}
Gap → {problem['gap']}
Impact if unsolved → {problem['impact']}

Project → [badass, memorable name - make it unique and catchy]
Stack → [exact tools only, e.g. Next.js + Supabase + Vercel]
Deploy → [one platform: Vercel / Railway / Render / Fly.io / Northflank]
Docs & Links →
• [Tool] → [url]
• [Tool] → [url]
• [Tool] → [url]
Why now → [one brutal truth sentence about market timing]
Potential → [realistic revenue, users, or portfolio power in 6-12 months]"""

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
        message = f"*FocusLock • Daily Spark*\n{timestamp} EAT\n\n{idea}\n\n_Next idea: Tomorrow at 10:00 AM EAT_"
        
        send_telegram(message)
        log_activity("Delivered project with Problem Statement + clean stack")
        print("✅ FocusLock complete")
    except Exception as e:
        print(f"❌ FocusLock crashed: {e}")
        raise
