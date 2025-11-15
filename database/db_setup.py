import sqlite3
import os
from datetime import datetime

class FinanceDB:
    def __init__(self, db_name="finance.db"):
        """Initialize database connection"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print(f"✅ Connected to {self.db_name}")
        
    def create_tables(self):
        """Create necessary tables"""
        self.connect()
        
        # Transactions table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                type TEXT NOT NULL
            )
        """)
        
        # User profile table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                monthly_income REAL,
                savings_goal REAL,
                risk_tolerance TEXT
            )
        """)
        
        self.conn.commit()
        print("✅ Tables created successfully!")
        
    def insert_transaction(self, date, category, amount, description, trans_type):
        """Insert a single transaction"""
        self.cursor.execute("""
            INSERT INTO transactions (date, category, amount, description, type)
            VALUES (?, ?, ?, ?, ?)
        """, (date, category, amount, description, trans_type))
        self.conn.commit()
        
    def get_all_transactions(self):
        """Get all transactions"""
        self.cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
        return self.cursor.fetchall()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✅ Database connection closed")

# Test the database
if __name__ == "__main__":
    db = FinanceDB()
    db.create_tables()
    db.close()