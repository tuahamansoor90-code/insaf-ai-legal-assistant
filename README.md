# ⚖️ InsafAI — Pakistan Citizen Rights & Consumer Law Assistant

**Project:** Citizen Rights & Legal Awareness Chatbot  
**Domain:** Pakistani Law, Consumer Rights, FIA Cybercrime & Tenant Protections  
**Student Name:** Muhammad Tuaha  
**Roll Number:** BSCS-F23-045  
**Interface:** Streamlit (`app.py`)  

---

## 📌 Project Overview
**InsafAI** is an intelligent, domain-specific legal awareness assistant designed for Pakistani citizens. It translates complex legal procedures and statutory provisions (such as the *Prevention of Electronic Crimes Act (PECA 2016)*, *Punjab Consumer Protection Act 2005*, *Tenancy & Rent Restriction Laws*, and *Police Order 2002*) into accessible, bilingual guidance (Roman Urdu and English).

The application incorporates a fuzzy Natural Language Understanding (NLU) engine using Python's standard `difflib.SequenceMatcher` to tolerate spelling mistakes, a persistent SQLite3 database for conversation audits and incident tracking, an automated statutory **15-Day Consumer Court Legal Notice Generator**, and optional Google Gemini LLM API integration.

---

## 🌟 Key Features

### 1. 💬 AI Legal Counselor (`st.chat_message`, `st.chat_input`)
- **Bilingual Conversational Interface:** Handles queries in both conversational English and everyday Roman Urdu (e.g., *"online fraud ho gaya, complaint kaise karein?"* or *"police bina warrant arrest kar sakti hai?"*).
- **Spelling Mistake Tolerance (`difflib`):** Correctly resolves typos (e.g. `'onlne frad'`, `'cybrcrime complnt'`, `'dokandar khrab chez'`) with confidence score reporting.
- **Intent & Confidence Badges:** Assistant messages display category, matched intent tag, and similarity percentage.
- **Transcript Export:** Download full chat logs as a `.txt` file with a single click.

### 2. 📜 15-Day Statutory Legal Notice Generator
- Generates an official, legally formatted **Notice under Section 28 of the Consumer Protection Act**.
- Users input complainant details, shopkeeper/store name, invoice number, purchase date, defect explanation, and claimed compensation.
- Produces a formal notice ready to be printed and dispatched via TCS/Registered Post before approaching Consumer Court.

### 3. 📝 Citizen Incident & Complaint Registry (SQLite Database)
- Users can log and record legal disputes (Online Scams, Defective Products, Landlord Disputes, Police Extortion) directly in the app.
- Automatically assigns a unique tracking token (e.g., `INSAF-PK-49210`).
- Stores drafts and records in `insaf_legal.db` with status updates.

### 4. 📞 Emergency Helplines & Web Portals
- Quick access directory to verified national helplines:
  - 🛡️ **FIA Cyber Crime Cell:** `1991` & [complaints.fia.gov.pk](https://complaints.fia.gov.pk)
  - 🚨 **Police Emergency:** `15`
  - 👩 **Women Protection / Harassment Helpline:** `1043` / `1099`
  - 🛣️ **National Highways & Motorway Police:** `130`
  - 🏛️ **Prime Minister's Citizen Portal (PCP)**
  - 🛒 **Consumer Protection Council (PCPC)**

### 5. 🤖 Optional Google Gemini API Connectivity
- Toggle advanced generative explanations for complex legal queries outside the local knowledge base by pasting a free Google Gemini API key into the sidebar.

---

## 🛠️ Technologies Used
- **Programming Language:** Python 3.10+ (Tested on Python 3.13)
- **Frontend / Framework:** Streamlit
- **Database:** SQLite3 (`insaf_legal.db`)
- **NLU / NLP Engine:** Python Standard Library (`difflib`, `re`, `json`, `datetime`, `urllib.request`)

---

## 📁 Project Architecture & File Layout
```text
d:/AI Lab Project/
│
├── app.py                         # Main Streamlit Web Application (streamlit run app.py)
├── knowledge_base.json            # External Self-Written Legal Knowledge Base (16 Intents, 100+ Patterns)
├── requirements.txt               # Dependencies file (streamlit)
├── VIVA_QUESTIONS_AND_ANSWERS.md  # Comprehensive Answers to All 9 Compulsory Viva Questions
├── backup_finance_bot/            # Complete backup of previous finance bot files
└── README.md                      # Official project documentation
```

---

## 🚀 How to Run the Project

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit Application
```bash
streamlit run app.py
```
*(Or run with `python -m streamlit run app.py`)*

The web app will launch automatically in your browser at `http://localhost:8501`.

---

## 💡 Sample Questions to Test
You can click any of these in the sidebar or type them in the chat input:
1. `Online fraud ho gaya, FIA complaint kaise karein?`
2. `Dukandar kharab cheez wapis nahi kar raha`
3. `How to send 15 days legal notice to seller?`
4. `Malik makan security deposit wapis nahi de raha`
5. `Police bina warrant ke giraftar kar sakti hai?`
6. `E-challan online kaise check aur pay karein?`
7. `Someone is blackmailing me on WhatsApp with pictures`
8. `What are emergency helpline numbers in Pakistan?`

---

## 🎓 Viva Defense Preparation
Review [`VIVA_QUESTIONS_AND_ANSWERS.md`](file:///d:/AI%20Lab%20Project/VIVA_QUESTIONS_AND_ANSWERS.md) for full detailed answers to the 9 mandatory university viva questions.
