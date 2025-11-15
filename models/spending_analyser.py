import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import numpy as np

class SpendingAnalyzer:
    def __init__(self, db_name="finance.db"):
        self.db_name = db_name
        
    def get_data(self):
        """Load data from database"""
        conn = sqlite3.connect(self.db_name)
        query = "SELECT * FROM transactions"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def categorize_spending(self):
        """Analyze spending by category"""
        df = self.get_data()
        expenses = df[df['type'] == 'expense']
        
        category_analysis = expenses.groupby('category').agg({
            'amount': ['sum', 'mean', 'count']
        }).round(2)
        
        return category_analysis
    
    def detect_unnecessary_spending(self):
        """Detect potentially unnecessary expenses"""
        df = self.get_data()
        expenses = df[df['type'] == 'expense']
        
        # Calculate average spending per category
        avg_by_category = expenses.groupby('category')['amount'].mean()
        
        # Flag expenses that are 50% above average
        unnecessary = []
        for _, row in expenses.iterrows():
            avg = avg_by_category[row['category']]
            if row['amount'] > avg * 1.5:
                unnecessary.append({
                    'date': row['date'],
                    'category': row['category'],
                    'amount': row['amount'],
                    'avg': round(avg, 2),
                    'excess': round(row['amount'] - avg, 2)
                })
        
        return unnecessary
    
    def get_monthly_summary(self):
        """Get monthly income vs expense summary"""
        df = self.get_data()
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        
        summary = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
        
        if 'expense' in summary.columns and 'income' in summary.columns:
            summary['savings'] = summary['income'] - summary['expense']
            summary['savings_rate'] = (summary['savings'] / summary['income'] * 100).round(2)
        
        return summary
    
    def get_spending_trends(self):
        """Analyze spending trends over time"""
        df = self.get_data()
        df['date'] = pd.to_datetime(df['date'])
        
        expenses = df[df['type'] == 'expense']
        daily_spending = expenses.groupby('date')['amount'].sum()
        
        # Calculate 7-day moving average
        trend = daily_spending.rolling(window=7).mean()
        
        return daily_spending, trend

# Test
if __name__ == "__main__":
    analyzer = SpendingAnalyzer()
    print("\n📊 Category Analysis:")
    print(analyzer.categorize_spending())
    
    print("\n⚠️  Unnecessary Spending:")
    unnecessary = analyzer.detect_unnecessary_spending()
    for item in unnecessary[:5]:  # Show first 5
        print(item)