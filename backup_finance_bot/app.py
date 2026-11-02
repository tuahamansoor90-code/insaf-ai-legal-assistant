"""
app.py - Personal Finance and Budgeting Helper Chatbot
Course: Python Chatbot Project (Mini Mids Guidelines)
Topic: No. 6 - Personal finance and budgeting helper
Student Name: Muhammad Tuaha
Roll Number: BSCS-F23-045

Design:
  Bespoke Modern Fintech Aesthetic (Obsidian & Emerald Glassmorphism)
  Featuring Google Font typography, custom styled chat cards, interactive
  chips, pulsing live badges, and streamlined academic credentials.
"""

from datetime import datetime
import difflib
import json
import os
import re
import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="FinanceBot • Personal Budgeting Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. ULTRA-PREMIUM MODERN FINTECH DESIGN SYSTEM (CSS Injection)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Import Google Modern Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Root Resets & Ambient Dark Theme */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #f1f5f9;
    }

    .stApp {
        background-color: #07090e;
        background-image: 
            radial-gradient(circle at 10% 15%, rgba(99, 102, 241, 0.10) 0%, transparent 45%),
            radial-gradient(circle at 90% 80%, rgba(16, 185, 129, 0.08) 0%, transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(14, 165, 233, 0.04) 0%, transparent 55%);
        background-attachment: fixed;
    }

    /* Hide standard Streamlit header & footer decorations */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    footer {visibility: hidden;}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0c0f17 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
        margin: 1.2rem 0 !important;
    }

    /* Student ID Card Badge */
    .student-badge-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 18px;
        box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
    }
    .student-badge-card .student-title {
        font-family: 'Outfit', sans-serif;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #818cf8;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .student-badge-card .student-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 4px;
    }
    .student-badge-card .student-roll {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.1);
        padding: 2px 8px;
        border-radius: 6px;
        display: inline-block;
        margin-top: 6px;
        border: 1px solid rgba(56, 189, 248, 0.2);
    }

    /* Main Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 26px 30px;
        margin-bottom: 24px;
        box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(16px);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #6366f1 0%, #38bdf8 50%, #10b981 100%);
    }
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 6px;
        font-weight: 400;
    }

    /* Status Pill Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.12);
        color: #34d399;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 20px;
        border: 1px solid rgba(16, 185, 129, 0.25);
    }
    .pulsing-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #10b981;
        box-shadow: 0 0 8px #10b981;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Interactive Sample Question Pills */
    .sample-pill-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 16px 0 24px 0;
    }
    .section-label {
        font-family: 'Outfit', sans-serif;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748b;
        margin-bottom: 8px;
    }

    /* Buttons Styling */
    .stButton button {
        background: rgba(30, 41, 59, 0.6) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 8px 14px !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-align: left !important;
    }
    .stButton button:hover {
        background: rgba(99, 102, 241, 0.15) !important;
        color: #ffffff !important;
        border-color: rgba(99, 102, 241, 0.4) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15) !important;
    }

    /* Download Button Emerald Accent */
    div[data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3) !important;
        text-align: center !important;
    }
    div[data-testid="stDownloadButton"] button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4) !important;
    }

    /* Chat Messages Overhauls */
    [data-testid="stChatMessage"] {
        padding: 16px 20px !important;
        border-radius: 16px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 20px -4px rgba(0, 0, 0, 0.35) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    /* Assistant (Bot) Bubble */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        background: rgba(17, 24, 39, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(12px) !important;
    }

    /* User Bubble */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: linear-gradient(135deg, rgba(67, 56, 202, 0.35) 0%, rgba(37, 99, 235, 0.35) 100%) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        backdrop-filter: blur(12px) !important;
    }

    /* Chat Input Bar Modernization */
    [data-testid="stChatInput"] {
        border-radius: 14px !important;
    }
    [data-testid="stChatInput"] textarea {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 14px !important;
        font-size: 0.95rem !important;
        padding: 12px 18px !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
    }

    /* Intent & Confidence Tag Pill */
    .meta-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 3px 10px;
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 10px;
    }
    .meta-tag b {
        color: #38bdf8;
    }
    .meta-tag .conf-high {
        color: #34d399;
        font-weight: 600;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #090d16;
    }
    ::-webkit-scrollbar-thumb {
        background: #1e293b;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #334155;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 3. KNOWLEDGE BASE & FUZZY NLU ENGINE (Rules 5 & Section 4 Guidelines)
# -----------------------------------------------------------------------------
KB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge_base.json")

@st.cache_data
def load_knowledge_base():
    """Load intents, patterns, and curated financial responses from external JSON."""
    if not os.path.exists(KB_FILE):
        return {"intents": [], "fallback_responses": []}
    with open(KB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

kb_data = load_knowledge_base()

def clean_text(text: str) -> str:
    """Preprocess input query: lowercase, strip punctuation, normalize whitespaces."""
    text_clean = re.sub(r"[^\w\s]", " ", text.lower())
    return " ".join(text_clean.split())

def calculate_similarity(s1: str, s2: str) -> float:
    """Compute similarity ratio using difflib to tolerate typos and spelling errors."""
    return difflib.SequenceMatcher(None, s1, s2).ratio()

def extract_salary_amount(text: str):
    """Detect dynamic salary queries (e.g. 'How much should I save from a 50,000 salary?')."""
    match = re.search(r"(\d[\d,]*)\s*(?:salary|income|kamai|rupees|rs)", text, re.I)
    if not match:
        match = re.search(r"(?:save\s+from|from\s+a)\s+(\d[\d,]*)", text, re.I)
    if match:
        try:
            val = float(match.group(1).replace(",", ""))
            if val >= 1000:
                return val
        except ValueError:
            pass
    return None

def generate_salary_breakdown(salary: float) -> str:
    """Generate tailored 50/30/20 budget breakdown for salary questions."""
    needs = salary * 0.50
    wants = salary * 0.30
    savings = salary * 0.20
    return (
        f"💡 **Recommended Budget for a Rs. {salary:,.0f} Salary (50/30/20 Rule):**\n\n"
        f"• **1. Needs (50% = Rs. {needs:,.0f}):** Mandatory essentials such as rent, groceries, utility bills, and transport.\n"
        f"• **2. Wants (30% = Rs. {wants:,.0f}):** Dining out, shopping, hobbies, personal care, and entertainment.\n"
        f"• **3. Savings & Investments (20% = Rs. {savings:,.0f}):** Emergency funds, liquid savings accounts, or mutual funds.\n\n"
        f"*Pro Tip:* Set up an automated recurring transfer of **Rs. {savings:,.0f}** on your payday so you save before spending!"
    )

def match_query(query: str):
    """
    Core intent matching engine:
    1. Dynamic salary calculations (Topic 6 core guideline query)
    2. Substring & Token Jaccard overlap
    3. Fuzzy Sequence Matching (difflib) for minor spelling mistakes
    4. Polite fallback response if unconfident
    """
    clean_q = clean_text(query)
    if not clean_q:
        return "Please enter a message or question.", "empty", 0.0

    # 1. Core Guideline Feature: Dynamic Salary Allocation
    salary = extract_salary_amount(query)
    if salary and ("save" in clean_q or "budget" in clean_q or "salary" in clean_q or "50" in clean_q):
        return generate_salary_breakdown(salary), "salary_saving_50k", 0.98

    best_intent = None
    best_score = 0.0
    query_tokens = set(clean_q.split())

    # 2. Match against knowledge_base.json intents
    for intent in kb_data.get("intents", []):
        for pattern in intent.get("patterns", []):
            clean_p = clean_text(pattern)

            # Exact Match
            if clean_q == clean_p:
                return intent["responses"][0], intent["tag"], 1.0

            # Substring Match
            if clean_p in clean_q or clean_q in clean_p:
                score = 0.92
                if score > best_score:
                    best_score = score
                    best_intent = intent

            # Token Overlap (Jaccard similarity)
            pattern_tokens = set(clean_p.split())
            if query_tokens and pattern_tokens:
                intersection = query_tokens.intersection(pattern_tokens)
                jaccard = len(intersection) / len(query_tokens.union(pattern_tokens))
                if jaccard > 0.5 and jaccard > best_score:
                    best_score = jaccard
                    best_intent = intent

            # Fuzzy Spelling Tolerance (difflib.SequenceMatcher)
            sim = calculate_similarity(clean_q, clean_p)
            if sim > 0.70 and sim > best_score:
                best_score = sim
                best_intent = intent

    # 3. High-confidence Domain Response
    if best_intent and best_score >= 0.65:
        return best_intent["responses"][0], best_intent["tag"], round(best_score, 2)

    # 4. Guideline Fallback Reply (Page 6 Interface Requirement 6)
    fallback = kb_data.get("fallback_responses", [
        "I am sorry, I did not understand that. Could you rephrase your question?"
    ])[0]
    return fallback, "fallback", round(best_score, 2)

# -----------------------------------------------------------------------------
# 4. SIDEBAR: CREDENTIALS, CHATBOT OVERVIEW & CONTROLS (Requirement 4 & 7)
# -----------------------------------------------------------------------------
with st.sidebar:
    # Student Accreditation Card
    st.markdown(
        """
        <div class="student-badge-card">
            <div class="student-title">🎓 University Submission</div>
            <div class="student-name">Muhammad Tuaha</div>
            <div class="student-roll">BSCS-F23-045</div>
            <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 8px;">
                <b>Course:</b> Python Chatbot Project<br>
                <b>Domain:</b> Topic 6 — Personal Finance
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Chatbot Overview Description
    st.markdown('<div class="section-label">📌 About The Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background: rgba(15, 23, 42, 0.6); padding: 12px 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.06); font-size: 0.84rem; color: #cbd5e1; line-height: 1.5;">
            An intelligent domain-specific assistant for <b>Personal Finance and Budgeting</b>. 
            Features fuzzy spelling tolerance, dynamic 50/30/20 salary modeling, and debt repayment frameworks.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">💡 Suggested Questions</div>', unsafe_allow_html=True)

    # Sample Question Buttons
    sample_questions = [
        "How much should I save from a 50,000 salary?",
        "What is the 50/30/20 rule?",
        "How to build an emergency fund?",
        "How can I cut my monthly expenses?",
        "How to pay off debt?",
        "Where to invest for beginners in Pakistan?",
        "How much should I spend on rent?",
        "What is savings ratio?",
    ]

    for sq in sample_questions:
        if st.button(f"💬 {sq}", key=f"side_btn_{sq}", use_container_width=True):
            st.session_state["query_input"] = sq

    st.markdown("---")

    # Clear Chat Button (Requirement 4)
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Download Conversation (Requirement 7: Additional Feature)
    if "messages" in st.session_state and len(st.session_state.messages) > 1:
        chat_text = f"=== PERSONAL FINANCE CHATBOT TRANSCRIPT ===\n"
        chat_text += f"Student: Muhammad Tuaha | Roll No: BSCS-F23-045\n"
        chat_text += f"Exported: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}\n\n"
        chat_text += "\n\n".join([f"[{m['role'].upper()}]: {m['content']}" for m in st.session_state.messages])
        
        st.download_button(
            label="📥 Export Conversation (.txt)",
            data=chat_text,
            file_name=f"FinanceBot_Transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )

# -----------------------------------------------------------------------------
# 5. MAIN CONVERSATION INTERFACE (Requirement 1, 2, 3, 5, 6, 7)
# -----------------------------------------------------------------------------

# Hero Banner with Verified Academic Metadata
st.markdown(
    """
    <div class="hero-banner">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
            <div>
                <h1 class="hero-title">💼 Personal Finance & Budgeting Helper</h1>
                <div class="hero-subtitle">Domain-Specific Python AI Chatbot with NLU Intent Classification</div>
            </div>
            <div class="status-badge">
                <span class="pulsing-dot"></span>
                <span>Topic 6 • Engine Active</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize Session State & Friendly Initial Greeting (Requirement 3 & 5)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Hello! Welcome to your Personal Finance & Budgeting Assistant.**\n\n"
                "I am here to help you plan your money, grow your savings, and master your cash flow:\n\n"
                "• **Salary Allocation:** Ask me *'How much should I save from a 50,000 salary?'*\n"
                "• **Budgeting Rules:** Inquire about the *50/30/20 rule* or *emergency funds*\n"
                "• **Debt & Investing:** Learn about *debt payoff strategies* or *beginner investments in Pakistan*\n"
                "• **Expense Optimization:** Ask how to *cut monthly living costs* or *budget for rent*\n\n"
                "Feel free to click any suggestion in the sidebar or type your financial question below!"
            ),
            "intent": "greeting",
            "confidence": 1.0,
        }
    ]

# Render Conversation History (Requirement 2 & 7)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Requirement 7: Confidence score and intent tag badge
        if msg["role"] == "assistant" and "intent" in msg:
            conf_val = msg.get("confidence", 1.0)
            conf_class = "conf-high" if conf_val >= 0.80 else ""
            st.markdown(
                f"""
                <div class="meta-tag">
                    <span>🎯 Intent: <b>{msg['intent']}</b></span>
                    <span>•</span>
                    <span class="{conf_class}">🔍 Match: <b>{conf_val * 100:.0f}%</b></span>
                </div>
                """,
                unsafe_allow_html=True
            )

# Check for Sidebar Quick-Button Trigger
user_prompt = None
if "query_input" in st.session_state:
    user_prompt = st.session_state.pop("query_input")
else:
    # Requirement 2: Chat Input Widget
    user_prompt = st.chat_input("Ask a finance question (e.g., How much should I save from a 50,000 salary?)...")

# Process Incoming Query
if user_prompt:
    # 1. Append and render user query
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # 2. Query Fuzzy NLU Engine
    bot_response, intent_tag, confidence = match_query(user_prompt)

    # 3. Append assistant response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response,
        "intent": intent_tag,
        "confidence": confidence,
    })

    # 4. Render assistant response with meta badge
    with st.chat_message("assistant"):
        st.markdown(bot_response)
        conf_class = "conf-high" if confidence >= 0.80 else ""
        st.markdown(
            f"""
            <div class="meta-tag">
                <span>🎯 Intent: <b>{intent_tag}</b></span>
                <span>•</span>
                <span class="{conf_class}">🔍 Match: <b>{confidence * 100:.0f}%</b></span>
            </div>
            """,
            unsafe_allow_html=True
        )
