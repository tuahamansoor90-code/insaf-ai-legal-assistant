# 🎓 Viva Defense Preparation Guide
**Project:** Personal Finance & Budgeting Chatbot (Domain 6)  
**Author:** Muhammad Tuaha (Roll No: BSCS-F23-045)  
**Interface:** Streamlit (`app.py`) & Tkinter Desktop (`main.py`)  

---

### Question 1: Why did you choose this domain, and who are the target users?
**Answer:**  
"I chose the **Personal Finance and Budgeting** domain because financial literacy and expense management are critical everyday challenges, especially for university students and young professionals managing a fixed monthly allowance or salary. In countries with high inflation, many individuals struggle to save consistently or budget their earnings. The target users are students, fresh graduates, and salaried individuals who need an accessible, automated assistant to track their cash flow, calculate salary savings allocations (like the 50/30/20 rule), and receive budget alert notifications before overspending."

---

### Question 2: How did you build your knowledge base, and how many intents or question-answer pairs does it contain?
**Answer:**  
"In accordance with Rule 5 of the project guidelines, the knowledge base was completely self-written and stored externally in `knowledge_base.json` rather than hardcoded in the script. It contains **13 distinct intent classes** with over **80 training pattern variations**, covering:
1. Greetings & Salutations (English and Roman Urdu)
2. Farewells & Gratitude
3. Salary savings breakdown (specifically addressing the sample question: *'How much should I save from a 50,000 salary?'*)
4. 50/30/20 Budgeting framework explanation and math
5. Emergency fund rules and calculation targets
6. Expense tracking methodologies
7. Actionable expense reduction strategies
8. Debt payoff methods (Avalanche vs Snowball)
9. Investment roadmaps for beginners in Pakistan (Mutual funds, National Savings, Index funds)
10. Housing & Rent 30% rule of thumb
11. Savings ratio mathematical formulas
12. Identity and capabilities of the bot
13. Domain-specific polite fallback responses."

---

### Question 3: Walk through what happens, step by step, from the moment the user presses Enter to the moment the reply appears.
**Answer:**  
"Here is the execution pipeline:
1. **Input Capture:** The user enters text via Streamlit's `st.chat_input` and presses Enter.
2. **Session Storage:** The query is appended to `st.session_state.messages` and instantly rendered on the screen inside `st.chat_message('user')`.
3. **Preprocessing:** The string passes to `ChatbotEngine.preprocess()`, which converts it to lowercase, strips punctuation, and normalizes whitespaces.
4. **Action & Transaction Check:** The engine checks using regex if the user logged an expense, income, or budget limit (e.g. *'I spent 500 on Food'*). If so, it updates the SQLite database (`budget_tracker.db`) and checks for 80% or 100% budget threshold alerts.
5. **Intent Matching & Similarity Scoring:** If it is a financial question, the engine matches tokens against `knowledge_base.json` using exact match, Jaccard token overlap, and `difflib.SequenceMatcher` to tolerate spelling mistakes.
6. **Confidence & Fallback:** If the similarity score is $\ge 0.65$, the corresponding domain response is selected. If an optional Google Gemini API key is configured, it queries the LLM; otherwise, it triggers a friendly domain fallback.
7. **Database Logging:** The conversation turn (user message, bot response, intent, confidence, timestamp) is logged to the SQLite `chat_logs` table.
8. **UI Rendering:** The assistant bubble renders via `st.chat_message('assistant')` with intent badges and confidence score metrics."

---

### Question 4: How does your chatbot handle a question it does not understand?
**Answer:**  
"When a query cannot be matched to any intent with a confidence score of at least 65%, the chatbot avoids crashing or returning raw errors. Instead, it activates a polite, domain-specific fallback response:  
*'I am sorry, I did not understand that. Could you please rephrase your question? You can ask me about budgeting rules, salary savings, emergency funds, or expense tracking.'*  
It also logs the fallback intent with a low confidence score to the SQLite database so the developer can review what users asked and expand the knowledge base."

---

### Question 5: How does your chatbot handle spelling mistakes?
**Answer:**  
"The chatbot uses Python's built-in `difflib.SequenceMatcher` algorithm inside `calculate_similarity()`. It calculates the Gestalt Pattern Matching ratio between the user's typed tokens and the knowledge base patterns. For example, if a user typos:
- `'50000 slary'` instead of `'50000 salary'`
- `'emrgency fnd'` instead of `'emergency fund'`
- `'budgt'` instead of `'budget'`  
The similarity score remains above 0.70, allowing the chatbot to correctly identify the user's intent despite typos without requiring external heavy machine learning models."

---

### Question 6: What happens if the user enters an empty message or only numbers?
**Answer:**  
- **Empty Message:** The `st.chat_input` widget rejects empty submissions by default. If bypassed via spaces, the engine detects an empty string after `strip()` and prompts the user: *'Please enter a message or question about budgeting, saving, or tracking expenses.'*
- **Only Numbers (e.g. '50000'):** The dynamic salary parser detects the numerical magnitude; if it's over 1,000, it interprets it as an inquiry on how to budget that salary amount and offers a 50/30/20 breakdown, or politely asks if the user meant to log an expense or income."

---

### Question 7: How would you add a new intent or question to your chatbot?
**Answer:**  
"Because of our modular decoupled architecture:
1. Open `knowledge_base.json`.
2. Add a new JSON object under `'intents'` with:
   - `'tag'`: the unique identifier (e.g. `'car_financing'`)
   - `'patterns'`: a list of sample questions users might ask
   - `'responses'`: the curated financial answers.
3. Save the file.  
No Python code changes or server recompilations are needed; the `ChatbotEngine` automatically re-reads the JSON and starts matching the new intent immediately."

---

### Question 8: What are the main limitations of your chatbot?
**Answer:**  
"1. **Domain Boundaries:** It is strictly tailored to personal finance and budgeting; it will not answer general queries outside this scope (e.g., weather or sports).
2. **Context Retention Depth:** While session history is stored and visible, multi-turn pronoun references (e.g., 'What about that?' referring to a previous topic) are handled via the recent DB context rather than a full transformer attention mechanism unless Gemini LLM mode is enabled.
3. **Local Deployment:** Currently runs locally on localhost via Streamlit rather than deployed on a public cloud URL."

---

### Question 9: How would you improve it if you had more time?
**Answer:**  
"1. **Bank Statement OCR / PDF Ingestion:** Add optical character recognition (`pytesseract` / `pdfplumber`) so users can upload their monthly bank PDF statements to auto-categorize transactions.
2. **Predictive Budget Forecasting:** Train a time-series model (ARIMA / Prophet) to forecast next month's utility and grocery bills based on historical spending.
3. **Voice Input/Output:** Integrate `SpeechRecognition` and `pyttsx3` for hands-free voice-driven budgeting.
4. **Cloud Database Sync:** Migrate local SQLite to PostgreSQL on Supabase or Google Cloud SQL for multi-device synchronization."
