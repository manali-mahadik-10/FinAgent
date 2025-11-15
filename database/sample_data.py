from db_setup import FinanceDB
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Generate 3 months of dummy transaction data"""
    
    db = FinanceDB()
    db.connect()
    
    # Categories and their typical amounts
    expense_categories = {
        "Food & Dining": (200, 800),
        "Transportation": (100, 500),
        "Shopping": (300, 1500),
        "Entertainment": (200, 1000),
        "Bills & Utilities": (500, 2000),
        "Healthcare": (200, 1000),
        "Education": (500, 2000),
        "Groceries": (1000, 3000)
    }
    
    income_sources = ["Salary", "Freelance", "Investment"]
    
    # Generate data for last 90 days
    start_date = datetime.now() - timedelta(days=90)
    
    print("🔄 Generating sample transactions...")
    
    for day in range(90):
        current_date = start_date + timedelta(days=day)
        date_str = current_date.strftime("%Y-%m-%d")
        
        # Generate 2-5 expenses per day
        num_expenses = random.randint(2, 5)
        for _ in range(num_expenses):
            category = random.choice(list(expense_categories.keys()))
            min_amt, max_amt = expense_categories[category]
            amount = round(random.uniform(min_amt, max_amt), 2)
            description = f"{category} expense"
            
            db.insert_transaction(date_str, category, amount, description, "expense")
        
        # Generate income (1st and 15th of month)
        if current_date.day == 1:
            db.insert_transaction(
                date_str, 
                "Salary", 
                50000.0, 
                "Monthly salary", 
                "income"
            )
        elif current_date.day == 15:
            if random.random() > 0.5:  # 50% chance of freelance income
                db.insert_transaction(
                    date_str,
                    "Freelance",
                    random.randint(5000, 15000),
                    "Freelance project payment",
                    "income"
                )
    
    # Insert user profile
    db.cursor.execute("""
        INSERT OR REPLACE INTO user_profile (id, monthly_income, savings_goal, risk_tolerance)
        VALUES (1, 50000, 15000, 'moderate')
    """)
    db.conn.commit()
    
    print(f"✅ Generated {db.cursor.execute('SELECT COUNT(*) FROM transactions').fetchone()[0]} transactions!")
    db.close()

if __name__ == "__main__":
    generate_sample_data()