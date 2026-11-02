"""
InsafAI - Pakistan Citizen Rights & Consumer Law Assistant
Author: Muhammad Tuaha (Roll No: BSCS-F23-045)
Course: Python Chatbot Project
Technologies: Python, Streamlit, SQLite3, difflib, json, re, datetime
"""

import streamlit as st
import json
import sqlite3
import re
import os
import random
from difflib import SequenceMatcher
from datetime import datetime
import urllib.request
import urllib.error

# ---------------------------------------------------------
# 1. Page Configuration & Custom CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="InsafAI - Citizen Rights & Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* Emerald & Slate Legal Palette */
    :root {
        --primary-legal: #0d5c3a;
        --accent-gold: #c29b38;
        --bg-soft: #f8fafc;
    }
    
    .legal-header {
        background: linear-gradient(135deg, #093f28 0%, #115e3c 60%, #1e3a2f 100%);
        padding: 24px 28px;
        border-radius: 14px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.12);
        border-left: 6px solid #c29b38;
    }
    
    .legal-badge {
        display: inline-block;
        padding: 4px 10px;
        font-size: 0.78rem;
        font-weight: 600;
        border-radius: 6px;
        background-color: #e2e8f0;
        color: #1e293b;
        margin-right: 6px;
    }
    
    .legal-badge-confidence {
        background-color: #d1fae5;
        color: #065f46;
        border: 1px solid #a7f3d0;
    }

    .legal-badge-intent {
        background-color: #fef3c7;
        color: #92400e;
        border: 1px solid #fde68a;
    }
    
    .helpline-card {
        background: white;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin-bottom: 12px;
        transition: transform 0.2s ease;
    }
    .helpline-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .disclaimer-box {
        background-color: #fffbeb;
        border: 1px solid #fef08a;
        border-left: 4px solid #eab308;
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 0.85rem;
        color: #713f12;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Database Management (SQLite3)
# ---------------------------------------------------------
DB_FILE = "insaf_legal.db"

def init_database():
    """Initializes SQLite database tables for chat audit logs and complaint records."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Audit trail for all conversations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            intent TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    
    # Registry for citizen complaint drafts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints_registry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_id TEXT UNIQUE NOT NULL,
            citizen_name TEXT NOT NULL,
            cnic TEXT NOT NULL,
            category TEXT NOT NULL,
            subject TEXT NOT NULL,
            details TEXT NOT NULL,
            evidence_summary TEXT,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_database()

def log_conversation_to_db(user_msg, bot_msg, intent, confidence):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO chat_logs (user_message, bot_response, intent, confidence, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (user_msg, bot_msg, intent, confidence, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database logging error: {e}")

def save_complaint_to_db(tracking_id, citizen_name, cnic, category, subject, details, evidence):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO complaints_registry (tracking_id, citizen_name, cnic, category, subject, details, evidence_summary, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (tracking_id, citizen_name, cnic, category, subject, details, evidence, "Draft / Ready to File", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_recent_complaints():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT tracking_id, citizen_name, category, subject, status, created_at FROM complaints_registry ORDER BY id DESC LIMIT 15")
    rows = cursor.fetchall()
    conn.close()
    return rows

# ---------------------------------------------------------
# 3. Knowledge Base & NLU Engine (difflib Fuzzy Matching)
# ---------------------------------------------------------
KB_PATH = "knowledge_base.json"

@st.cache_data
def load_knowledge_base():
    if os.path.exists(KB_PATH):
        with open(KB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"intents": []}

knowledge_base = load_knowledge_base()

class LegalChatbotEngine:
    def __init__(self, kb):
        self.kb = kb
        self.stop_words = {
            "is", "a", "an", "the", "in", "on", "at", "to", "for", "of", "and", "or",
            "me", "mera", "meri", "kya", "hai", "hain", "ke", "ki", "ko", "ka", "par",
            "se", "karein", "karna", "please", "can", "you", "tell", "mujhe", "batao"
        }

    def preprocess(self, text: str) -> str:
        """Cleans, normalizes, and removes punctuation."""
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        return " ".join(text.split())

    def get_tokens(self, text: str) -> set:
        """Tokenizes text filtering basic conversational filler words."""
        cleaned = self.preprocess(text)
        tokens = set(cleaned.split())
        meaningful = tokens - self.stop_words
        return meaningful if meaningful else tokens

    def calculate_similarity(self, user_text: str, pattern: str) -> float:
        """
        Combines SequenceMatcher (string Gestalt pattern matching for typos)
        and Jaccard token overlap similarity.
        """
        clean_user = self.preprocess(user_text)
        clean_pat = self.preprocess(pattern)

        # 1. Exact string match
        if clean_user == clean_pat or clean_pat in clean_user:
            return 1.0

        # 2. difflib SequenceMatcher (tolerant to typos like 'frad', 'cybrcrime', 'agreemnt')
        seq_sim = SequenceMatcher(None, clean_user, clean_pat).ratio()

        # 3. Token Jaccard overlap
        user_tokens = self.get_tokens(user_text)
        pat_tokens = self.get_tokens(pattern)
        intersection = user_tokens.intersection(pat_tokens)
        union = user_tokens.union(pat_tokens)
        jaccard_sim = len(intersection) / len(union) if union else 0.0

        # Weighted combination: 60% Token overlap + 40% String typo similarity
        combined = (jaccard_sim * 0.60) + (seq_sim * 0.40)
        return max(seq_sim, combined)

    def find_intent(self, user_input: str):
        """Scans the external knowledge base to find the best matching intent and score."""
        best_intent = None
        best_score = 0.0
        matched_category = "General"

        for intent in self.kb.get("intents", []):
            if intent["tag"] == "fallback":
                continue
            for pattern in intent.get("patterns", []):
                score = self.calculate_similarity(user_input, pattern)
                if score > best_score:
                    best_score = score
                    best_intent = intent["tag"]
                    matched_category = intent.get("category", "General")

        return best_intent, best_score, matched_category

    def query_gemini_api(self, prompt: str, api_key: str) -> str:
        """Optional Google Gemini LLM fallback using lightweight standard library urllib."""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            sys_instruction = (
                "You are InsafAI, an expert in Pakistani Citizen Rights, Consumer Law, Cybercrime (PECA 2016), "
                "Tenant Acts, and Police Order. Give helpful, legally accurate, concise responses in easy-to-understand "
                "English or Roman Urdu with relevant law references and emergency helplines. Include a brief disclaimer."
            )
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": f"{sys_instruction}\n\nUser Question: {prompt}"}]
                    }
                ]
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=12) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"*(Gemini API fallback error: {str(e)} — Falling back to local rule-based response)*"

    def respond(self, user_input: str, gemini_key: str = "") -> dict:
        """Determines best response, logs to SQLite, and returns metadata."""
        intent, confidence, category = self.find_intent(user_input)

        # Confidence Threshold: 0.50
        if intent and confidence >= 0.50:
            for item in self.kb.get("intents", []):
                if item["tag"] == intent:
                    reply = random.choice(item["responses"])
                    log_conversation_to_db(user_input, reply, intent, confidence)
                    return {
                        "response": reply,
                        "intent": intent,
                        "confidence": confidence,
                        "category": category,
                        "source": "Local Rule-Based NLU (difflib)"
                    }

        # If low confidence and Gemini API key is provided, query Gemini
        if gemini_key and len(gemini_key.strip()) > 15:
            gemini_reply = self.query_gemini_api(user_input, gemini_key.strip())
            log_conversation_to_db(user_input, gemini_reply, "gemini_generative", 0.95)
            return {
                "response": gemini_reply,
                "intent": "generative_llm",
                "confidence": 0.95,
                "category": "AI Legal Consultation",
                "source": "Google Gemini 1.5 Flash"
            }

        # Otherwise trigger fallback intent
        fallback_item = next((i for i in self.kb.get("intents", []) if i["tag"] == "fallback"), None)
        fallback_reply = (
            random.choice(fallback_item["responses"])
            if fallback_item
            else "I'm sorry, I could not understand your legal question. Please rephrase in simpler terms."
        )
        log_conversation_to_db(user_input, fallback_reply, "fallback", confidence)
        return {
            "response": fallback_reply,
            "intent": "fallback",
            "confidence": confidence,
            "category": "General",
            "source": "Fallback Handler"
        }

engine = LegalChatbotEngine(knowledge_base)

# ---------------------------------------------------------
# 4. Session State Initialization
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Assalam-o-Alaikum! Main **InsafAI** hoon — aapka Pakistan Citizen Rights & Legal Awareness Assistant. 🇵🇰⚖️\n\n"
                "Aap mujhse pooch sakte hain:\n"
                "• **Online Fraud & Cybercrime:** FIA 1991 complaint procedure, blackmailed ho rahe hain toh kya karein.\n"
                "• **Consumer Protection:** Kharab product ka 15-day legal notice, Consumer Court case.\n"
                "• **Tenant & Rental Rights:** Security deposit wapsi, eviction notice period rules.\n"
                "• **Traffic & Police Rights:** E-challan checking, arrest rights & 24-hour magistrate rule."
            ),
            "intent": "greeting",
            "confidence": 1.0,
            "category": "General",
            "source": "System Welcome"
        }
    ]

# ---------------------------------------------------------
# 5. Sidebar Interface
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/120/scales--v1.png", width=70)
    st.markdown("## ⚖️ InsafAI Portal")
    st.caption("**Domain:** Citizen Rights & Legal Awareness (Pakistan)")
    st.markdown("---")

    st.markdown("### 🎓 Student Profile")
    st.markdown("""
    - **Name:** Muhammad Tuaha
    - **Roll No:** BSCS-F23-045
    - **Course:** Python AI Chatbot Project
    - **Technology:** Streamlit, SQLite, NLU (`difflib`)
    """)
    st.markdown("---")

    st.markdown("### 💡 Common Legal Questions")
    sample_queries = [
        "Online fraud ho gaya, FIA complaint kaise karein?",
        "Dukandar kharab cheez wapis nahi kar raha",
        "How to send 15 days legal notice to seller?",
        "Malik makan security deposit wapis nahi de raha",
        "Police bina warrant ke giraftar kar sakti hai?",
        "E-challan online kaise check aur pay karein?",
        "Someone is blackmailing me on WhatsApp with pictures",
        "What are emergency helpline numbers in Pakistan?"
    ]
    for q in sample_queries:
        if st.button(f"📌 {q}", key=f"btn_{q[:15]}", use_container_width=True):
            st.session_state.user_trigger = q

    st.markdown("---")
    st.markdown("### 🤖 Optional Generative AI")
    gemini_api_key = st.text_input(
        "Google Gemini API Key (Optional)",
        type="password",
        placeholder="AIzaSy...",
        help="Paste a free Google Gemini key to enable advanced AI answers for questions outside local knowledge base."
    )

    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Chat Export Button
    if st.session_state.messages:
        chat_text = "\n".join([f"[{m.get('role', '').upper()}]: {m.get('content', '')}" for m in st.session_state.messages])
        st.download_button(
            label="📥 Download Chat Transcript",
            data=chat_text,
            file_name=f"InsafAI_Legal_Chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )

# ---------------------------------------------------------
# 6. Main Interface Layout (Navigation Tabs)
# ---------------------------------------------------------
st.markdown("""
<div class="legal-header">
    <h1 style="margin:0; font-size: 2.1rem; color: #ffffff;">⚖️ InsafAI: Pakistan Citizen Rights & Consumer Law Assistant</h1>
    <p style="margin: 6px 0 0 0; opacity: 0.9; font-size: 1.05rem; color: #f1f5f9;">
        Aam Shehri Ki Aasan Legal Rehnumai • Cybercrime (FIA) • Consumer Court • Tenant Rights • Police Laws
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer-box">
    ⚠️ <strong>Qanooni Wazahath (Legal Disclaimer):</strong> InsafAI aam shehriyon ki agahi aur guidance ke liye banaya gaya hai. Yeh official Pakistani qawaneen par mabni information fraham karta hai magar kisi professional registered wakeel (advocate) ki legal counsel ka mutabadil nahi hai.
</div>
""", unsafe_allow_html=True)

tab_chat, tab_notice, tab_complaint, tab_helplines = st.tabs([
    "💬 AI Legal Counselor",
    "📜 15-Day Legal Notice Generator",
    "📝 Citizen Complaint Registry",
    "📞 Emergency Helplines & Portals"
])

# ---------------------------------------------------------
# Tab 1: AI Legal Counselor (Chat Interface)
# ---------------------------------------------------------
with tab_chat:
    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🧑‍💼" if msg["role"] == "user" else "⚖️"):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and "intent" in msg:
                conf = msg.get("confidence", 0.0) * 100
                st.markdown(
                    f"<div style='margin-top: 8px;'>"
                    f"<span class='legal-badge legal-badge-intent'>🏷️ Intent: {msg.get('intent', 'N/A')}</span>"
                    f"<span class='legal-badge legal-badge-confidence'>🎯 Confidence: {conf:.1f}%</span>"
                    f"<span class='legal-badge'>📁 Category: {msg.get('category', 'General')}</span>"
                    f"<span class='legal-badge'>⚙️ {msg.get('source', 'Local Engine')}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

    # Process prompt from sidebar button or chat input
    user_query = None
    if "user_trigger" in st.session_state and st.session_state.user_trigger:
        user_query = st.session_state.user_trigger
        st.session_state.user_trigger = None
    else:
        user_query = st.chat_input("Apna qanooni masla ya sawal yahan likhein (e.g. 'online scam ho gaya, kya karoon?')...")

    if user_query:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user", avatar="🧑‍💼"):
            st.markdown(user_query)

        # Generate response using engine
        with st.spinner("Qanooni dastawez aur relevant acts scan kiye ja rahe hain..."):
            result = engine.respond(user_query, gemini_api_key)

        # Display assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["response"],
            "intent": result["intent"],
            "confidence": result["confidence"],
            "category": result["category"],
            "source": result["source"]
        })
        st.rerun()

# ---------------------------------------------------------
# Tab 2: 15-Day Consumer Legal Notice Generator
# ---------------------------------------------------------
with tab_notice:
    st.subheader("📜 Consumer Court 15-Day Legal Notice Generator")
    st.write(
        "Pakistani Consumer Protection Acts ke tehat Consumer Court jane se pehle dukandar/seller ko "
        "**15 din ka formal Legal Notice** bhejna qanoonan zaroori hota hai. Neeche diye gaye form ko fill karein "
        "aur ready-to-print legal notice download karein:"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 👤 Complainant (Aapki) Details")
        c_name = st.text_input("Aapka Poora Naam", "Muhammad Ali")
        c_address = st.text_input("Aapka Rihaishi Pata (Address)", "House #12, Street 4, F-8, Islamabad")
        c_cnic = st.text_input("Aapka CNIC Number", "37405-1234567-1")
        c_phone = st.text_input("Aapka Mobile Number", "0300-1234567")

    with col2:
        st.markdown("#### 🏬 Seller / Company Details")
        s_name = st.text_input("Dukandar / Company ka Naam", "ABC Electronics / Online Store")
        s_address = st.text_input("Dukan / Office ka Pata", "Shop #45, Hafeez Centre, Gulberg III, Lahore")
        p_name = st.text_input("Product / Service ka Naam", "Samsung LED TV 55 Inch")
        p_price = st.text_input("Ada ki gayi Raqam (PKR)", "125,000")
        p_date = st.date_input("Kharidari ki Tareekh (Purchase Date)").strftime("%d-%B-%Y")
        invoice_no = st.text_input("Receipt / Invoice Number", "INV-98234")

    st.markdown("#### ⚠️ Defect & Claim Details")
    defect_desc = st.text_area(
        "Nuqsan ya Fraud ki Mukhtasir Tafseel (Defect / Grievance)",
        "The screen display started flickering within 2 days of delivery. Upon contacting the seller, warranty service was refused and the return policy was denied."
    )
    damages_claimed = st.text_input("Harjana / Damages Claim Amount (PKR)", "50,000")

    if st.button("⚡ Generate Official Legal Notice", type="primary", use_container_width=True):
        legal_notice_draft = f"""LEGAL NOTICE UNDER SECTION 28 OF THE CONSUMER PROTECTION ACT
(DISPATCHED VIA REGISTERED POST ACKNOWLEDGEMENT DUE / TCS)

Date: {datetime.now().strftime("%d-%B-%Y")}

TO:
{s_name}
{s_address}

FROM:
{c_name} (CNIC: {c_cnic})
{c_address}
Contact: {c_phone}

SUBJECT: STATUTORY 15-DAYS LEGAL NOTICE FOR DEFECTIVE PRODUCT / DEFICIENT SERVICES, REPLACEMENT, AND DAMAGES

Respected Sir/Madam,

Under instructions and on behalf of my statutory rights as a consumer under the Consumer Protection Act, I hereby serve upon you this formal 15-day Legal Notice stating as follows:

1. That on {p_date}, the undersigned purchased '{p_name}' against an invoice/receipt number {invoice_no} by paying a total consideration of PKR {p_price}/- in good faith.

2. That upon testing and using the aforementioned product, the undersigned discovered serious inherent defects, namely:
   "{defect_desc}"

3. That the undersigned immediately approached your store/representative demanding rectification, replacement, or refund in accordance with consumer warranty norms. However, your response was wholly dismissive, illegal, and contrary to the Consumer Protection Act.

4. That selling defective, counterfeit, or substandard products and refusing statutory remedy constitutes a blatant unfair trade practice and deficiency in product warranty. The unlawful conduct of your establishment has caused grave mental anguish, financial agony, and inconvenience to the undersigned.

DEMANDS / RELIEF SOUGHT:
You are hereby called upon through this 15-day statutory Legal Notice to:
a) Refund the full purchase consideration of PKR {p_price}/- OR provide a brand new, fully certified replacement;
b) Pay a sum of PKR {damages_claimed}/- on account of damages, mental harassment, and transport/communication costs.

TAKE NOTICE:
If you fail to redress the aforementioned grievance within FIFTEEN (15) DAYS of the receipt of this legal notice, the undersigned shall be constrained to initiate formal proceedings before the Honourable CONSUMER COURT / CONSUMER PROTECTION TRIBUNAL at your sole risk, cost, and consequences, including heavy fines and imprisonment as per law.

Yours faithfully,

___________________________
{c_name}
Complainant / Consumer
CNIC: {c_cnic}
Mobile: {c_phone}
Address: {c_address}
"""
        st.success("✅ Legal Notice kamyabi se generate ho gaya hai!")
        st.text_area("📜 Generated Notice Preview", legal_notice_draft, height=350)

        st.download_button(
            label="📄 Download Ready-to-Print Legal Notice (.txt)",
            data=legal_notice_draft,
            file_name=f"Legal_Notice_{s_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )

# ---------------------------------------------------------
# Tab 3: Citizen Complaint Registry (SQLite Database)
# ---------------------------------------------------------
with tab_complaint:
    st.subheader("📝 Citizen Incident & Complaint Registry")
    st.write(
        "Aap kisi bhi qanooni incident (Online Fraud, Cyber Harassment, Police Extortion, Consumer Dispute) "
        "ka draft record InsafAI ke internal database me mehfooz kar sakte hain aur tracking ID haasil kar sakte hain:"
    )

    with st.form("complaint_form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            comp_name = st.text_input("Shikayat-kuninda Ka Naam (Full Name)*")
            comp_cnic = st.text_input("CNIC Number (e.g. 35202-xxxxxxx-x)*")
            comp_cat = st.selectbox(
                "Maslay Ka Category*",
                ["FIA Cybercrime & Online Fraud", "Consumer Court / Defective Product", "Tenant / Landlord Dispute", "Police Misconduct / Traffic Violation", "Workplace Harassment", "Other"]
            )
        with col_b:
            comp_subject = st.text_input("Maslay Ka Unwaan (Subject / Title)*")
            comp_evidence = st.text_input("Mojood Proofs (Screenshots, Bank SMS, Receipts, Audio)")

        comp_details = st.text_area("Waqiaye Ki Mukammal Tafseel (Incident Details)*")
        submitted = st.form_submit_button("💾 Save Incident Draft to Registry", use_container_width=True)

        if submitted:
            if comp_name and comp_cnic and comp_subject and comp_details:
                track_id = f"INSAF-PK-{random.randint(10000, 99999)}"
                save_complaint_to_db(track_id, comp_name, comp_cnic, comp_cat, comp_subject, comp_details, comp_evidence)
                st.success(f"🎉 Complaint successfully registered with Tracking ID: **{track_id}**")
            else:
                st.error("Barahe karam tamam required (*) fields fill karein!")

    st.markdown("---")
    st.markdown("#### 📋 Saved Complaint Registry (SQLite Persistence)")
    records = get_recent_complaints()
    if records:
        table_data = []
        for r in records:
            table_data.append({
                "Tracking ID": r[0],
                "Name": r[1],
                "Category": r[2],
                "Subject": r[3],
                "Status": r[4],
                "Created At": r[5]
            })
        st.dataframe(table_data, use_container_width=True)
    else:
        st.info("Abhi tak koi complaint draft register nahi hua.")

# ---------------------------------------------------------
# Tab 4: Emergency Helplines & Web Portals
# ---------------------------------------------------------
with tab_helplines:
    st.subheader("📞 Pakistan Official Legal & Emergency Helplines")
    st.write("Emergency ya foran qanooni imdad ke liye in official government numbers aur portals par rabta karein:")

    col_h1, col_h2 = st.columns(2)
    
    with col_h1:
        st.markdown("""
        <div class="helpline-card">
            <h3 style="color: #0d5c3a; margin-top:0;">🛡️ FIA Cyber Crime Cell (NR3C)</h3>
            <p><strong>UAN Helpline:</strong> <code>1991</code> (Toll-Free, 24/7)</p>
            <p><strong>Online Complaint Portal:</strong> <a href="https://complaints.fia.gov.pk" target="_blank">complaints.fia.gov.pk</a></p>
            <p style="font-size:0.85rem; color:#64748b;">Report online financial scams, blackmailing, unauthorized pictures, and hacking.</p>
        </div>
        
        <div class="helpline-card">
            <h3 style="color: #0d5c3a; margin-top:0;">🚨 Police Emergency</h3>
            <p><strong>Helpline:</strong> <code>15</code></p>
            <p><strong>Anti-Corruption Punjab / Sindh:</strong> <code>1098</code> / <code>1128</code></p>
            <p style="font-size:0.85rem; color:#64748b;">Immediate emergency rescue, theft, robbery, or illegal detention.</p>
        </div>
        
        <div class="helpline-card">
            <h3 style="color: #0d5c3a; margin-top:0;">👩 Women Protection Helpline</h3>
            <p><strong>Punjab Women Helpline:</strong> <code>1043</code></p>
            <p><strong>Federal Mohtasib (FOSPAH):</strong> <code>051-9262143</code></p>
            <p style="font-size:0.85rem; color:#64748b;">Workplace harassment, domestic abuse, and legal aid for women.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_h2:
        st.markdown("""
        <div class="helpline-card">
            <h3 style="color: #0d5c3a; margin-top:0;">🛒 Consumer Protection Courts</h3>
            <p><strong>Punjab Consumer Portal:</strong> <a href="https://pcpc.punjab.gov.pk" target="_blank">pcpc.punjab.gov.pk</a></p>
            <p><strong>Court Fees:</strong> <code>Free of Cost (Zero Fee)</code></p>
            <p style="font-size:0.85rem; color:#64748b;">File claims against dishonest sellers, expired products, or unfulfilled warranties.</p>
        </div>

        <div class="helpline-card">
            <h3 style="color: #0d5c3a; margin-top:0;">🛣️ National Highways & Motorway Police</h3>
            <p><strong>Helpline:</strong> <code>130</code></p>
            <p style="font-size:0.85rem; color:#64748b;">Motorway assistance, highway breakdown, accidents, and route advisory.</p>
        </div>

        <div class="helpline-card">
            <h3 style="color: #0d5c3a; margin-top:0;">🏛️ Prime Minister's Citizen Portal (PCP)</h3>
            <p><strong>Platform:</strong> Citizen Portal Android & iOS App</p>
            <p style="font-size:0.85rem; color:#64748b;">Direct complaints to federal and provincial departments and municipal authorities.</p>
        </div>
        """, unsafe_allow_html=True)
