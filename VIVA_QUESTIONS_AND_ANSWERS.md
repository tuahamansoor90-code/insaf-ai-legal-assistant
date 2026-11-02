# 🎓 Viva Defense Preparation Guide — InsafAI
**Project:** InsafAI — Pakistan Citizen Rights & Consumer Law Assistant  
**Author:** Muhammad Tuaha (Roll No: BSCS-F23-045)  
**Interface:** Streamlit (`app.py`)  
**Database:** SQLite3 (`insaf_legal.db`)  
**NLU Engine:** Python Standard Library (`difflib.SequenceMatcher` + Jaccard token overlap)  

---

### Question 1: Why did you choose this domain, and who are the target users?
**Answer:**  
"I chose the **Citizen Rights and Consumer Law** domain because legal awareness and access to justice in Pakistan are major everyday challenges. The vast majority of citizens do not know their basic rights when faced with online scams (FIA cybercrime), defective goods sold by dishonest merchants (Consumer Court), landlord security deposit disputes, or arbitrary police harassment. Hiring lawyers is expensive, and legal acts are written in intimidating legal jargon.

The target users are ordinary citizens, university students, online shoppers, tenants, and small business consumers who need immediate, plain-language guidance in Roman Urdu or English on how to exercise their constitutional and statutory rights without paying heavy advocate fees."

---

### Question 2: How did you build your knowledge base, and how many intents or question-answer pairs does it contain?
**Answer:**  
"In compliance with project guidelines, the knowledge base is stored externally in `knowledge_base.json` rather than hardcoded inside Python scripts. It contains **16 distinct intents** with over **100 pattern variations** covering English and Roman Urdu questions:
1. `greeting` — Conversational welcomes and introductory guidance
2. `goodbye` — Courteous wrap-up and empowerment advice
3. `identity_and_capabilities` — InsafAI overview and domain scope
4. `cybercrime_online_fraud` — Online scams, bank OTP fraud, EasyPaisa/JazzCash scams (PECA 2016)
5. `cybercrime_harassment_blackmail` — Online blackmailing, unauthorized picture leaks, cyber stalking
6. `fia_complaint_procedure` — Step-by-step FIA NR3C reporting, website (complaints.fia.gov.pk), helpline 1991
7. `consumer_rights_defective_product` — Defective goods, illegal 'no return' signs, consumer statutory rights
8. `consumer_legal_notice_procedure` — Statutory 15-day notice, free Consumer Court filings without a lawyer
9. `tenant_rental_rights` — Security deposit recovery, 1-2 month notice period, rent increment limits
10. `traffic_rules_and_echallan` — E-challan portal verification, payment methods, vehicle impound rules
11. `police_arrest_and_citizen_rights` — 24-hour Magistrate rule (CrPC 61), search warrants, FIR rights (CrPC 154)
12. `workplace_women_harassment` — Protection Against Workplace Harassment Act, Federal Ombudsman (FOSPAH)
13. `emergency_helplines` — Official emergency numbers (Police 15, FIA 1991, Motorway 130, Women 1043)
14. `right_to_information_rti` — Article 19-A Constitution, obtaining government project/budget records
15. `bounced_cheque_law` — Dishonoured cheque consequences under Section 489-F PPC
16. `fallback` — Domain-specific polite fallback guidance."

---

### Question 3: Walk through what happens, step by step, from the moment the user presses Enter to the moment the reply appears.
**Answer:**  
"Here is the execution pipeline:
1. **Input Capture:** The user enters a question into Streamlit's `st.chat_input` and hits Enter.
2. **Session Storage:** The query is added to `st.session_state.messages` and rendered immediately via `st.chat_message('user')`.
3. **Preprocessing:** The string passes through `LegalChatbotEngine.preprocess()`, which converts it to lowercase, strips punctuation marks with regex (`re.sub(r'[^\w\s]', ' ', text)`), and removes conversational filler stop-words.
4. **Fuzzy NLU & Similarity Scoring:** The engine computes two metrics against all patterns in `knowledge_base.json`:
   - `SequenceMatcher.ratio()` (Gestalt pattern matching for string typo tolerance).
   - Jaccard token overlap similarity.
   - A weighted score is computed: $Score = (Jaccard \times 0.60) + (SequenceMatcher \times 0.40)$.
5. **Confidence & Fallback Decision:**
   - If the best match score $\ge 0.50$ (50%), the matching legal response is randomly selected.
   - If score $< 0.50$ and the user provided a Google Gemini API key, it invokes `query_gemini_api()`.
   - Otherwise, it invokes the domain-specific fallback handler.
6. **Database Logging:** The entire conversation turn (user message, bot response, intent, confidence, timestamp) is logged into the SQLite table `chat_logs`.
7. **UI Rendering:** The assistant bubble is rendered with intent badge, confidence percentage, category, and matching source tag."

---

### Question 4: How does your chatbot handle a question it does not understand?
**Answer:**  
"When an input fails to reach the 50% confidence threshold, the chatbot never crashes or emits an unhandled exception. It activates a polite, domain-specific fallback response:  
*'Mujhe afsos hai, main aapka sawal poori tarah nahi samajh saka. Aap mujhse Pakistan ke Consumer Court, Online Cybercrime (FIA), Tenant/Kirayedar Laws, Traffic E-Challan, ya Police Arrest Rights ke baare me pooch sakte hain.'*  
Furthermore, it logs this fallback event into the SQLite `chat_logs` table with the low confidence score, enabling the administrator/developer to audit unhandled queries and continually expand the knowledge base."

---

### Question 5: How does your chatbot handle spelling mistakes?
**Answer:**  
"The chatbot implements Python's built-in `difflib.SequenceMatcher` algorithm. Rather than demanding rigid character-by-character string equality, `SequenceMatcher` calculates the ratio of the longest contiguous matching subsequences. For example:
- `'onlne frad'` correctly matches `'online fraud'` with over 90% confidence.
- `'cybrcrime complnt'` correctly maps to the FIA cybercrime procedure intent.
- `'dokandar khrab chez'` matches the consumer defective product intent.  
Combined with token-based Jaccard similarity, it tolerates typos, transposed characters, and informal Roman Urdu spellings."

---

### Question 6: What is the role of SQLite in your project, and what data does it store?
**Answer:**  
"SQLite3 provides zero-configuration, lightweight, serverless relational persistence in `insaf_legal.db`. It manages two dedicated tables:
1. `chat_logs`: Contains `(id, user_message, bot_response, intent, confidence, timestamp)`. This provides a complete audit trail of user interactions, enabling offline analytical review of common citizen concerns.
2. `complaints_registry`: Stores user incident drafts with columns `(tracking_id, citizen_name, cnic, category, subject, details, evidence_summary, status, created_at)`. This allows citizens to formally draft, save, and review incident reports (with unique tracking IDs like `INSAF-PK-49210`) before lodging them with the FIA or police."

---

### Question 7: Explain the difference between rule-based chatbots and LLM-based chatbots, and how your project combines both.
**Answer:**  
"A **Rule-based chatbot** maps user input to predefined patterns and verified responses. Its advantage is absolute reliability, zero hallucinations, fast local execution without internet, and total legal accuracy. Its limitation is that it cannot answer questions outside its predefined patterns.

An **LLM-based chatbot** (like Google Gemini) uses deep neural networks to generate human-like text on open-ended topics, but can occasionally hallucinate or generate non-binding legal claims.

**InsafAI uses a Hybrid Architecture:**
- By default, it runs completely offline using rule-based NLU with `difflib` pattern matching for guaranteed Pakistani statutory accuracy.
- However, if the user configures an optional Gemini API key in the sidebar, queries that fall below the local confidence threshold are seamlessly routed to Gemini 1.5 Flash with a specialized system prompt enforcing Pakistani legal context."

---

### Question 8: How does the 15-Day Consumer Legal Notice Generator work?
**Answer:**  
"Under Section 28 of the Punjab Consumer Protection Act 2005 (and equivalent provincial statutes), a consumer cannot directly approach the Consumer Court without first giving the respondent 15 days written notice of the claim.

The **Legal Notice Generator** in Tab 2 provides an interactive form where the citizen inputs their particulars, the vendor's details, invoice date, defect explanation, and demanded damages. When submitted, it automatically compiles a legally compliant, formal statutory notice complete with statutory clauses, limitation warnings, and claim relief. The user can preview and download the formatted notice as a `.txt` file ready to be printed and sent via registered post."

---

### Question 9: What are some potential future enhancements for this project?
**Answer:**  
"Potential future enhancements include:
1. **Urdu Nastaliq Script Support:** Adding native Urdu font rendering alongside Roman Urdu.
2. **Audio / Speech-to-Text (Voice Bot):** Allowing illiterate or semi-literate citizens to speak their problem in Urdu and listen to spoken advice.
3. **Automated PDF Export with Signatures:** Exporting legal notices with official formatting and watermarks as downloadable PDF documents.
4. **GPS Nearest Police Station / Consumer Court Locator:** Using geolocation to point the citizen to the exact address and contact officer of their nearest court or FIA center."
