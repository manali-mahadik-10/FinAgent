import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import sys, os

# add parent path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_setup import FinanceDB
from models.spending_analyser import SpendingAnalyzer
from models.predictor import ExpensePredictor
from agents.finance_agent import FinanceAgent

# ----- Page setup -----
st.set_page_config(
    page_title="FinAgent - Your AI Finance Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling
st.markdown(
    """
<style>
.main-header {font-size:2.4rem;font-weight:700;text-align:center;color:#1976D2;margin:1rem 0;}
.subtitle {text-align:center;color:#666;margin-bottom:1rem;}
.metric-card{background:#1976D2;padding:1rem;border-radius:10px;color:white;text-align:center;}
</style>
""",
    unsafe_allow_html=True,
)

# ----- Session state -----
if "agent" not in st.session_state:
    st.session_state.agent = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "agent_initialized" not in st.session_state:
    st.session_state.agent_initialized = False

# ----- Header -----
st.markdown("<div class='main-header'>💰 FinAgent</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Your Personal AI Finance Decision Assistant</div>",
    unsafe_allow_html=True,
)

# ----- Sidebar -----
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/000000/money-bag.png", width=140)
    st.header("⚙️ Control Panel")

    if not st.session_state.agent_initialized:
        if st.button("🚀 Initialize AI Agent", use_container_width=True):
            with st.spinner("Loading AI Agent..."):
                try:
                    st.session_state.agent = FinanceAgent()
                    st.session_state.agent_initialized = True
                    st.success("✅ Agent Ready")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error initializing agent: {e}")
    else:
        st.success("✅ Agent Active")
        if st.button("🔄 Restart Agent", use_container_width=True):
            st.session_state.agent = None
            st.session_state.agent_initialized = False
            st.session_state.chat_history = []
            st.rerun()

    st.divider()
    st.header("📊 Financial Overview")
    try:
        analyzer = SpendingAnalyzer()
        summary = analyzer.get_monthly_summary()
        if not summary.empty:
            latest = summary.iloc[-1]
            st.metric("💸 Expenses", f"₹{latest.get('expense',0):,.0f}")
            st.metric("💵 Income", f"₹{latest.get('income',0):,.0f}")
            st.metric(
                "💰 Savings",
                f"₹{latest.get('savings',0):,.0f}",
                delta=f"{latest.get('savings_rate',0):.1f}%",
            )
    except:
        st.info("Generate data to see financial summary.")

    st.divider()
    st.markdown("### 💡 Sample Queries")
    st.markdown(
        """
- “Analyze my spending this month”
- “Where can I cut unnecessary expenses?”
- “If I invest ₹5000 at 8% for 2 years compounded monthly?”
- “Predict my next month’s expenses”
"""
    )

# ----- Tabs -----
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["💬 AI Assistant", "📊 Analytics", "🔮 Predictions", "➕ Add Transaction", "📚 About"]
)

# =========================
# TAB 1: Chat Interface
# =========================
with tab1:
    st.header("💬 Chat with Your AI Finance Assistant")

    if not st.session_state.agent_initialized:
        st.warning("⚠️ Initialize the AI agent from sidebar first.")
    else:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("Ask about your finances...")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                try:
                    reply = st.session_state.agent.chat(user_input)
                except Exception as e:
                    reply = f"Error: {e}"
            st.session_state.chat_history.append(
                {"role": "assistant", "content": reply}
            )
            st.rerun()

# =========================
# TAB 2: Analytics
# =========================
with tab2:
    st.header("📊 Analytics Dashboard")
    try:
        analyzer = SpendingAnalyzer()
        cat_data = analyzer.categorize_spending()
        if not cat_data.empty:
            st.subheader("💳 Spending by Category")

            # Colorful circular pie chart
            category_totals = cat_data[("amount", "sum")]
            colors = plt.cm.Paired(range(len(category_totals)))
            fig, ax = plt.subplots(figsize=(6, 6))
            wedges, texts, autotexts = ax.pie(
                category_totals,
                labels=category_totals.index,
                autopct="%1.1f%%",
                startangle=90,
                colors=colors,
                textprops={"fontsize": 9, "color": "black"},
            )
            for autotext in autotexts:
                autotext.set_color("white")
                autotext.set_fontweight("bold")
            ax.set_title("Spending Distribution", fontsize=13, fontweight="bold")
            st.pyplot(fig)
        else:
            st.info("Add transactions to view analytics.")
    except Exception as e:
        st.error(f"Error loading analytics: {e}")

# =========================
# TAB 3: Predictions
# =========================
with tab3:
    st.header("🔮 Future Expense Predictions")
    try:
        predictor = ExpensePredictor()
        predictor.train_model()
        predictions = predictor.predict_next_month()
        if predictions:
            df = pd.DataFrame(
                {
                    "Category": list(predictions.keys()),
                    "Predicted (₹)": [
                        v["monthly_total"] for v in predictions.values()
                    ],
                }
            )
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            st.info("No prediction data yet.")
    except Exception as e:
        st.error(f"Error generating predictions: {e}")

# =========================
# TAB 4: Add Transaction
# =========================
with tab4:
    st.header("➕ Add New Transaction")

    with st.form("transaction_form"):
        col1, col2 = st.columns(2)
        with col1:
            trans_type = st.selectbox("Transaction Type", ["expense", "income"])
            category = st.text_input("Category")
            amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
        with col2:
            date = st.date_input("Date", datetime.now())
            desc = st.text_input("Description", "")
        submit = st.form_submit_button("💾 Save Transaction")
        if submit:
            try:
                db = FinanceDB()
                db.connect()
                db.insert_transaction(
                    date.strftime("%Y-%m-%d"),
                    category,
                    amount,
                    desc,
                    trans_type,
                )
                db.close()
                st.success("✅ Transaction added successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")

    st.divider()
    st.subheader("🧾 Recent Transactions")
    try:
        db = FinanceDB()
        db.connect()
        rows = db.cursor.execute(
            "SELECT date, category, amount, description, type FROM transactions ORDER BY date DESC LIMIT 10"
        ).fetchall()
        db.close()
        if rows:
            df = pd.DataFrame(
                rows, columns=["Date", "Category", "Amount", "Description", "Type"]
            )
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No transactions found.")
    except Exception as e:
        st.error(f"Error loading transactions: {e}")

# =========================
# TAB 5: About
# =========================
with tab5:
    st.header("📚 About FinAgent")
    st.markdown(
        """
**FinAgent** is your AI-powered personal finance assistant 🧠💰  
It helps you track spending, predict future expenses, and make better money decisions.

### ⚙️ Built With
- **Python + Streamlit** for the interface  
- **SQLite** for secure local data storage  
- **LangChain + Groq Llama 3.3** for the AI engine  
- **Matplotlib + Pandas** for visual insights  

### 💡 Features
- Real-time AI conversation about finances  
- Transaction tracking  
- Expense analytics and visualization  
- Predictive financial forecasting  

Developed by **Manali Prakash Mahadik** 💙  
Version **1.1 (2025)**  
"""
    )

# ----- Footer -----
st.divider()
st.markdown(
    "<p style='text-align:center;color:#999;'>FinAgent v1.1 — Powered by Groq Llama 3.3 | Built with Streamlit</p>",
    unsafe_allow_html=True,
)
