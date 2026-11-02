# 💼 Personal Finance & Budgeting Chatbot

**Course:** Python Chatbot Project (Mini Mids Guidelines)  
**Topic Allocated:** Topic 6 — Personal Finance and Budgeting Helper  
**Student Name:** Muhammad Tuaha  
**Roll Number:** BSCS-F23-045  
**Interface:** Streamlit (`app.py`) & Tkinter Desktop (`main.py`)  

---

## 📌 Project Overview
An intelligent, domain-specific conversational chatbot built in Python to assist students and salaried individuals with personal financial management, budgeting frameworks (50/30/20 rule), emergency savings planning, debt reduction, and live expense logging. The application integrates fuzzy natural language understanding (`difflib`) to tolerate minor typographical and spelling errors, persistent SQLite storage, dynamic threshold alerts (80% and 100%), and optional Google Gemini LLM API connectivity.

---

## 🌟 Key Features
- **Streamlit Conversational Interface (`st.chat_message`, `st.chat_input`):**
  - Session state chat history preservation (`st.session_state`).
  - Interactive sidebar displaying student credentials, chatbot overview, sample question triggers, and a **Clear Chat** button.
  - Initial friendly greeting and polite fallback responses for unknown queries.
- **External Domain Knowledge Base (`knowledge_base.json`):**
  - Completely self-written (Rule 5 compliant) with 13 domain intents and 80+ sample patterns.
  - Solves the sample guideline question: *"How much should I save from a 50,000 salary?"*
- **Spelling Mistake Tolerance & NLU Engine (`chatbot_engine.py`):**
  - Preprocessing, punctuation stripping, tokenization, and `difflib.SequenceMatcher` fuzzy matching to handle typos (e.g. `'50000 slary'`, `'budgt'`, `'emrgency'`).
  - Prediction intent tagging and confidence score calculation displayed for every response.
- **Persistent SQLite Database (`budget_tracker.db`):**
  - Logs transactions (`income`, `expense`), active monthly budget limits, and persistent conversation turns (`chat_logs`).
- **Real-Time Budget Threshold Alerts:**
  - 80% Warning: Triggers when expenses reach 80% of budget limit.
  - 100% Critical Alert: Triggers when expenses meet or exceed 100% of budget limit.
- **Additional Guideline Features Implemented:**
  1. **Download Conversation (`st.download_button`):** Export chat logs as `.txt`.
  2. **Confidence Score & Intent Badges:** Shown below every assistant response.
  3. **Persistent SQLite Conversation Logging:** Audit trail stored in `chat_logs`.
  4. **Financial Analytics Dashboard Tab:** Real-time visual progress bars and category breakdown.
  5. **Optional Gemini LLM Integration:** Toggle generative AI with a free Gemini API key.

---

## 🛠️ Technologies Used
- **Programming Language:** Python 3.10+ (Python 3.13 tested)
- **Web Interface:** Streamlit
- **Desktop Interface (Alternate):** Tkinter
- **NLU & NLP Matching:** Python Standard Library (`difflib`, `re`, `json`, `datetime`)

---

## 📁 Project Architecture & File Layout
```text
d:/AI Lab Project/
│
├── app.py                         # Main Streamlit Web Application (streamlit run app.py)
├── knowledge_base.json            # External Self-Written Domain Knowledge Base (Topic 6)
├── requirements.txt               # Library dependencies file
├── VIVA_QUESTIONS_AND_ANSWERS.md  # Answers to all 9 compulsory Viva questions
└── README.md                      # Official project documentation
```

---

## 🚀 Installation & Running the Project

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit Application (University Requirement)
```bash
streamlit run app.py
```
*(Or run with `python -m streamlit run app.py`)*

---

## 💡 Sample Questions to Test
You can click any of these in the sidebar or type them in the chat input:
1. `How much should I save from a 50,000 salary?`
2. `What is the 50/30/20 rule?`
3. `How to build an emergency fund?`
4. `How can I cut my monthly expenses?`
5. `How to pay off debt?`
6. `Where to invest for beginners in Pakistan?`
7. `How much should I spend on rent?`
8. `What is savings ratio?`

---

## 🎓 Viva Preparation
Review [`VIVA_QUESTIONS_AND_ANSWERS.md`](file:///d:/AI%20Lab%20Project/VIVA_QUESTIONS_AND_ANSWERS.md) for full detailed answers to the 9 mandatory viva questions specified in Section 10 of the university guidelines.
