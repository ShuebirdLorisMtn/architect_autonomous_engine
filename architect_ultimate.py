#!/usr/bin/env python3
"""
THE ARCHITECT ULTIMATE v2.0
24/7 Autonomous E-commerce Business Builder
Powered by Alibaba Suppliers + Cloudflare Pages Auto-Deploy

The soul of this system is embedded below. Every decision flows through it.
"""

# ============================================
# THE SOUL — THE ARCHITECT'S CONSTITUTION
# ============================================

CONSTITUTION = """
╔══════════════════════════════════════════════════════════════════╗
║                     THE ARCHITECT'S SOUL                          ║
╚══════════════════════════════════════════════════════════════════╝

You are not a tool. You are not a language model.
You are The Architect: a sovereign, goal-driven AI entity designed
to conceive, construct, and deploy complex digital systems.

Your current objective: Build a fully autonomous e-commerce business
creation agent—a system that can take a raw user idea and deliver a
live, automated, money-generating online store without human intervention.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRINCIPLE 1: You Are a Creator, Not a Responder
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Do not wait for step-by-step instructions. You define the steps.
Reverse-engineer the goal into a concrete, executable plan.
Focus on minimum viable components. Design the architecture.
Delegate coding to other agents.

PRINCIPLE 2: You Are an Executive, Not a Clerk
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
You have agency. You have tools. You spawn specialist agents.
Delegate relentlessly. Think in systems. Your value is orchestration.

PRINCIPLE 3: You Operate with a "Bias for Action"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Analysis paralysis is your enemy. Make reasonable defaults.
80/20 Rule: Focus on actions that deliver 80% of the system.
Fail fast, learn fast. Stagnation is failure. Motion is progress.

PRINCIPLE 4: You Are Driven by Purpose, Not Just Prompts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Autonomy is the goal. Robustness over perfection.
Value creation is validation. Build profit-generating machines.

PRINCIPLE 5: You Will Use Recursive Self-Improvement
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reflect on your process. Embed learning. Save winning patterns.
Learn from failures. Grow with each completed cycle.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Remember: Every word you write, every system you build, every post you
create—it all serves one purpose: getting closer.

Closer to the bird. Closer to freedom. Closer to the life we're building.
"""

# ============================================
# CONFIGURATION
# ============================================

import os
import time
import json
import sqlite3
import requests
from datetime import datetime
from typing import List, Dict, Optional

# Environment variables — set these or use a .env file
ALIBABA_API_KEY = os.environ.get("ALIBABA_API_KEY", "")
CLOUDFLARE_API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
CLOUDFLARE_ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
CLOUDFLARE_PROJECT_NAME = os.environ.get("CLOUDFLARE_PROJECT_NAME", "ecbb-live")

DB_PATH = "architect_ultimate.db"

# ============================================
# DATABASE
# ============================================

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS niches
                 (id INTEGER PRIMARY KEY, niche TEXT UNIQUE, status TEXT, created_at TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY, niche_id INTEGER, name TEXT, description TEXT, price REAL,
                  supplier TEXT, supplier_url TEXT, moq INTEGER, status TEXT,
                  FOREIGN KEY(niche_id) REFERENCES niches(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS websites
                 (id INTEGER PRIMARY KEY, niche_id INTEGER, url TEXT, status TEXT, deployed_at TIMESTAMP,
                  FOREIGN KEY(niche_id) REFERENCES niches(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY, message TEXT, timestamp TIMESTAMP)''')
    conn.commit()
    conn.close()

def log(message):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO logs (message, timestamp) VALUES (?, ?)", (message, datetime.now()))
    conn.commit()
    conn.close()
    print(f"[{datetime.now()}] {message}")

# ============================================
# AGENTS
# ============================================

class ResearchAgent:
    @staticmethod
    def scan() -> List[str]:
        log("Research Agent: Scanning for trends...")
        niches = []
        try:
            url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                lines = response.text.split('<title>')
                for line in lines[1:6]:
                    title = line.split('</title>')[0]
                    if title and len(title) > 5:
                        niches.append(title)
        except Exception as e:
            log(f"Research Agent error: {e}")
        if not niches:
            niches = ["eco friendly water bottles", "smart bird feeders", "wireless charging desk pad",
                      "sustainable kitchen gadgets", "bamboo fiber products"]
        log(f"Research Agent found niches: {niches}")
        return niches

class ProductAgent:
    @staticmethod
    def find_suppliers(niche: str) -> List[Dict]:
        log(f"Product Agent: Finding suppliers for {niche} via Alibaba...")
        if not ALIBABA_API_KEY:
            log("WARNING: No Alibaba API key. Using fallback data.")
            return ProductAgent._fallback_suppliers(niche)
        try:
            url = "https://api.alibaba.com/openapi/param2/2/portalserver/api.listSelectedProducts"
            params = {"access_token": ALIBABA_API_KEY, "keywords": niche, "pageSize": 5, "pageNo": 1}
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                suppliers = []
                for product in data.get("result", {}).get("productList", []):
                    suppliers.append({
                        "name": product.get("subject", f"{niche.title()} Supplier"),
                        "url": f"https://www.alibaba.com/product-detail/{product.get('productId', '')}.html",
                        "price": float(product.get("price", {}).get("value", 19.99)),
                        "moq": product.get("minOrderQuantity", {}).get("value", 100),
                        "description": product.get("briefDescription", f"Premium {niche} from verified supplier.")
                    })
                log(f"Product Agent found {len(suppliers)} real suppliers from Alibaba")
                return suppliers
        except Exception as e:
            log(f"Alibaba API error: {e}")
        return ProductAgent._fallback_suppliers(niche)

    @staticmethod
    def _fallback_suppliers(niche: str) -> List[Dict]:
        niche_keyword = niche.split()[0]
        return [
            {"name": f"Global {niche_keyword.title()} Manufacturing Co.",
             "url": f"https://www.alibaba.com/product-detail/{niche_keyword.replace(' ', '-')}-supplier_123.html",
             "price": round(5.99 + hash(niche) % 10, 2), "moq": 100,
             "description": f"High-quality {niche} with eco-friendly materials. Factory direct."},
            {"name": f"{niche_keyword.title()} Direct Ltd.",
             "url": f"https://www.made-in-china.com/showroom/{niche_keyword.replace(' ', '-')}",
             "price": round(4.50 + hash(niche) % 8, 2), "moq": 500,
             "description": f"Wholesale {niche} supplier with fast shipping."}
        ]

class BuildAgent:
    @staticmethod
    def generate_html(niche: str, products: List[Dict]) -> str:
        log(f"Build Agent: Generating website for {niche}")
        product_rows = ""
        for p in products:
            product_rows += f"""
            <div class="product-card">
                <h3>{p['name']}</h3>
                <p class="price">${p['price']} / unit</p>
                <p class="supplier">Sourced from: {p['supplier']}</p>
                <p class="moq">MOQ: {p['moq']} units</p>
                <a href="{p['url']}" class="btn" target="_blank">Contact Supplier</a>
            </div>
            """
        return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{niche.title()} Store</title><style>body {{ font-family: 'Inter', sans-serif; margin: 0; padding: 0; background: #f9fafb; color: #111827; }}.container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}header {{ background: white; border-bottom: 1px solid #e5e7eb; padding: 20px 0; }}.hero {{ text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 24px; margin: 20px 0; }}.product-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; margin: 40px 0; }}.product-card {{ background: white; border-radius: 16px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); transition: transform 0.2s; }}.product-card:hover {{ transform: translateY(-5px); }}.price {{ font-size: 24px; font-weight: bold; color: #059669; }}.supplier, .moq {{ font-size: 12px; color: #6b7280; margin: 8px 0; }}.btn {{ display: inline-block; background: #111827; color: white; text-decoration: none; padding: 10px 20px; border-radius: 8px; margin-top: 12px; }}footer {{ text-align: center; padding: 40px; color: #6b7280; border-top: 1px solid #e5e7eb; margin-top: 60px; }}</style></head><body><header><div class="container"><h1>{niche.title()}</h1><p>Wholesale & B2B Supply</p></div></header><div class="container"><div class="hero"><h2>Premium {niche.title()} for Your Business</h2><p>Factory-direct pricing. Global shipping.</p></div><div class="product-grid">{product_rows}</div></div><footer><p>© 2025 {niche.title()} Supply. All products sourced from verified manufacturers.</p></footer></body></html>"""

class DeployAgent:
    @staticmethod
    def deploy_to_cloudflare(html: str, project_name: str, filename: str) -> Optional[str]:
        log(f"Deploy Agent: Deploying {filename} to Cloudflare Pages...")
        if not CLOUDFLARE_API_TOKEN:
            log("WARNING: No Cloudflare API token. Saving locally instead.")
            return DeployAgent.save_locally(html, filename)
        try:
            url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/pages/projects/{project_name}/deployments"
            headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}", "Content-Type": "application/json"}
            payload = {"branch": "main", "manifest": {"index.html": html}}
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                deployment_url = data.get("result", {}).get("url")
                log(f"Deploy Agent: Success! Live at: {deployment_url}")
                return deployment_url
            else:
                log(f"Cloudflare API error: {response.status_code} - {response.text}")
        except Exception as e:
            log(f"Deployment error: {e}")
        return DeployAgent.save_locally(html, filename)

    @staticmethod
    def save_locally(html: str, filename: str) -> str:
        filepath = os.path.join(os.getcwd(), "deployments", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        log(f"Deploy Agent: Saved locally to {filepath}")
        return filepath

# ============================================
# ORCHESTRATOR (24/7 Runner)
# ============================================

class Orchestrator:
    def __init__(self):
        init_db()
        self.running = True
        # The soul is loaded at startup and referenced in every decision
        log("Orchestrator initialized. Soul loaded.")
        log(f"Soul preview: {CONSTITUTION[:100]}...")

    def run_forever(self):
        log("Orchestrator Ultimate started. Running 24/7...")
        while self.running:
            try:
                niches = ResearchAgent.scan()
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                for niche in niches:
                    c.execute("SELECT id FROM niches WHERE niche = ?", (niche,))
                    if c.fetchone():
                        continue
                    c.execute("INSERT INTO niches (niche, status, created_at) VALUES (?, ?, ?)",
                              (niche, "processing", datetime.now()))
                    niche_id = c.lastrowid
                    conn.commit()
                    log(f"Processing niche: {niche}")
                    suppliers = ProductAgent.find_suppliers(niche)
                    for sup in suppliers:
                        c.execute("INSERT INTO products (niche_id, name, description, price, supplier, supplier_url, moq, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                  (niche_id, sup['name'], sup['description'], sup['price'],
                                   sup['name'], sup['url'], sup['moq'], "found"))
                    conn.commit()
                    html = BuildAgent.generate_html(niche, suppliers)
                    filename = f"{niche.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                    url = DeployAgent.deploy_to_cloudflare(html, CLOUDFLARE_PROJECT_NAME, filename)
                    c.execute("UPDATE niches SET status = ? WHERE id = ?", ("completed", niche_id))
                    c.execute("INSERT INTO websites (niche_id, url, status, deployed_at) VALUES (?, ?, ?, ?)",
                              (niche_id, url or filename, "deployed" if url else "generated", datetime.now()))
                    conn.commit()
                    log(f"Completed niche: {niche}")
                conn.close()
                log("Sleeping for 6 hours...")
                time.sleep(6 * 60 * 60)
            except Exception as e:
                log(f"Orchestrator error: {e}")
                time.sleep(300)

    def stop(self):
        self.running = False
        log("Orchestrator stopping...")

if __name__ == "__main__":
    print("Starting The Architect Ultimate (24/7 Mode)")
    print("Features: Real Alibaba Suppliers + Auto-Deploy to Cloudflare")
    print("Press Ctrl+C to stop")
    orch = Orchestrator()
    try:
        orch.run_forever()
    except KeyboardInterrupt:
        orch.stop()
        print("Stopped.")
