import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType, Tool

import sys
sys.path.append('..')

from models.spending_analyser import SpendingAnalyzer
from models.predictor import ExpensePredictor

load_dotenv()


class FinanceAgent:
    """Autonomous AI Agent powered by Groq’s Llama-3.1 models"""

    def __init__(self):
        # Core tools
        self.analyzer = SpendingAnalyzer()
        self.predictor = ExpensePredictor()
        self.predictor.train_model()

        # ✅ Groq LLM (Free, active model)
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",  # new working model
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0,
            max_tokens=1024,
        )

        # Conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        # Tools
        tools = [
            Tool(
                name="Analyze_Spending",
                func=self.analyze_spending_tool,
                description="Analyze user's spending patterns by category.",
            ),
            Tool(
                name="Detect_Unnecessary_Spending",
                func=self.detect_unnecessary_tool,
                description="Find unnecessary or excessive expenses.",
            ),
            Tool(
                name="Predict_Next_Month",
                func=self.predict_next_month_tool,
                description="Predict next month's expenses using ML.",
            ),
            Tool(
                name="Monthly_Summary",
                func=self.monthly_summary_tool,
                description="Give income vs expense summary and savings rate.",
            ),
        ]

        # Initialize Agent
        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent_type=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=False,
            handle_parsing_errors=True,
        )

    # =============== TOOL METHODS ======================

    def analyze_spending_tool(self, _: str) -> str:
        category_analysis = self.analyzer.categorize_spending()
        if category_analysis.empty:
            return "No spending data available yet."
        result = "📊 **Spending by Category:**\n\n"
        for category, data in category_analysis.iterrows():
            result += (
                f"**{category}** → "
                f"₹{data[('amount', 'sum')]:.2f} total "
                f"({int(data[('amount', 'count')])} txns)\n"
            )
        return result

    def detect_unnecessary_tool(self, _: str) -> str:
        unnecessary = self.analyzer.detect_unnecessary_spending()
        if not unnecessary:
            return "✅ No excessive spending detected."
        result = f"⚠️ Found {len(unnecessary)} potential overspends:\n"
        for item in unnecessary[:10]:
            result += (
                f"- {item['date']}: {item['category']} ₹{item['amount']:.2f} "
                f"(₹{item['excess']:.2f} above avg)\n"
            )
        return result

    def predict_next_month_tool(self, _: str) -> str:
        predictions = self.predictor.predict_next_month()
        result = "🔮 **Next Month Predictions:**\n\n"
        total = 0
        for cat, val in predictions.items():
            result += f"- {cat}: ₹{val['monthly_total']:.2f}\n"
            total += val["monthly_total"]
        result += f"\n**Total Predicted:** ₹{total:.2f}"
        return result

    def monthly_summary_tool(self, _: str) -> str:
        summary = self.analyzer.get_monthly_summary()
        if summary.empty:
            return "No monthly summary data found."
        result = "📅 **Monthly Financial Summary:**\n\n"
        for month, data in summary.iterrows():
            result += (
                f"{month}: Income ₹{data.get('income',0):.2f}, "
                f"Expense ₹{data.get('expense',0):.2f}, "
                f"Savings ₹{data.get('savings',0):.2f} "
                f"({data.get('savings_rate',0):.1f}%)\n"
            )
        return result

    # =============== MAIN CHAT INTERFACE ===============

    def chat(self, user_message: str) -> str:
        """Run conversation through the agent"""
        try:
            response = self.agent.run(user_message)
            return response
        except Exception as e:
            return f"I encountered an error: {e}"


# =============== TESTING ===============
if __name__ == "__main__":
    print("🤖 Initializing FinanceAgent with Groq Llama-3.1…")
    agent = FinanceAgent()
    while True:
        msg = input("\nYou: ")
        if msg.lower() in ["exit", "quit", "bye"]:
            break
        print("\nFinAgent:", agent.chat(msg))
