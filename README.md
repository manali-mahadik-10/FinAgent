✅ FINAGENT — Finance Agentic AI Assistant
Your Personal Finance Analyst Powered by Groq LLM + Streamlit + SQLite

📌 Overview

FinAgent is an Agentic AI-powered finance assistant capable of performing:

Personal finance analytics

Expense predictions

Budget advice

Real-time conversation

Transaction tracking

Category-wise spending analysis

Built with Streamlit, Groq LLM, and SQLite, it acts as a simple, fast, and intelligent finance companion that users can chat with to get explanations, predictions, and insights.

🚀 Key Features
💬 AI Chat Assistant

Ask anything related to your finances:

“Analyze my monthly spending”

“Predict my next month’s expenses”

“Explain compound interest”

“How can I optimize my budget?”

📊 Analytics Dashboard

Category-wise spending visualization

Past month summary

Financial health metrics

Colorful charts for clarity

🔮 Predictions Engine

ML-powered monthly expense prediction

Category-wise breakdown

Clean tabular UI

🧾 Transaction Manager

Add income/expense entries

Stored in a local SQLite DB

Auto updates analytics + predictions

🏗️ Tech Stack
Component	Technology Used
Frontend	Streamlit
LLM / AI Engine	Groq API (Llama 3.1/3.3 Models)
Backend	Python
Database	SQLite3
Analytics	Pandas + Matplotlib
Memory / AI Logic	Custom Reasoning Pipeline
📁 Project Structure
FinAgent/
│── app.py
│── requirements.txt
│── README.md
│── agents/
│   └── finance_agent.py
│── database/
│   └── db_setup.py
│── models/
│   ├── spending_analyser.py
│   ├── predictor.py
│── assets/ (optional)
└── venv/ (ignored)

⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/YOUR-USERNAME/FinAgent.git
cd FinAgent

2️⃣ Create Virtual Environment
python -m venv venv

3️⃣ Activate venv

Windows

venv\Scripts\activate

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Add Groq API Key

Create .env file:

GROQ_API_KEY=your_api_key_here

6️⃣ Run App
streamlit run app.py

🤖 How It Works

The AI pipeline is simple but powerful:

User asks a financial question

Query is routed to FinanceAgent

Groq LLM analyzes context and past chat

SQLite data is fetched (transactions, categories, patterns)

LLM generates insights using real numbers

Response is displayed instantly in Streamlit

This creates a real-time interactive finance advisor.

🖼️ Screenshots

(Insert your Streamlit app screenshots here)

[IMAGE PLACEHOLDER – HOME SCREEN]
[IMAGE PLACEHOLDER – ANALYTICS]
[IMAGE PLACEHOLDER – PREDICTIONS]
[IMAGE PLACEHOLDER – CHAT]

🧠 Possible Improvements

Add machine learning for trend forecasting

Add OCR to read receipts

Add voice-enabled chat

Export financial reports as PDF

Add bank integration (UPI, CSV, API-based)

🏁 Conclusion

FinAgent demonstrates how Agentic AI + finance + database intelligence can come together to build a practical, real-world tool. It is lightweight, scalable, and perfect for students, developers, and fintech research.

⭐ Support

If you like this project, please ⭐ the repo — it motivates me to build more!
