import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import sqlite3
from datetime import datetime, timedelta

class ExpensePredictor:
    def __init__(self, db_name="finance.db"):
        self.db_name = db_name
        self.model = LinearRegression()
        self.label_encoder = LabelEncoder()
        
    def prepare_data(self):
        """Prepare data for ML model"""
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query("SELECT * FROM transactions WHERE type='expense'", conn)
        conn.close()
        
        df['date'] = pd.to_datetime(df['date'])
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_month'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        
        # Encode category
        df['category_encoded'] = self.label_encoder.fit_transform(df['category'])
        
        return df
    
    def train_model(self):
        """Train prediction model"""
        df = self.prepare_data()
        
        # Features: day_of_week, day_of_month, month, category
        X = df[['day_of_week', 'day_of_month', 'month', 'category_encoded']]
        y = df['amount']
        
        self.model.fit(X, y)
        print("✅ Model trained successfully!")
        
        return self.model.score(X, y)  # R² score
    
    def predict_next_month(self):
        """Predict next month's expenses by category"""
        df = self.prepare_data()
        
        # Get unique categories
        categories = df['category'].unique()
        
        next_month = datetime.now() + timedelta(days=30)
        predictions = {}
        
        for category in categories:
            category_encoded = self.label_encoder.transform([category])[0]
            
            # Predict for middle of next month (day 15)
            X_pred = np.array([[
                next_month.weekday(),  # day of week
                15,  # day of month
                next_month.month,  # month
                category_encoded  # category
            ]])
            
            predicted_amount = self.model.predict(X_pred)[0]
            
            # Estimate monthly total (assuming ~15 transactions per month per category)
            avg_transactions = df[df['category'] == category].groupby(
                df['date'].dt.to_period('M')
            ).size().mean()
            
            monthly_prediction = predicted_amount * avg_transactions
            
            predictions[category] = {
                'per_transaction': round(predicted_amount, 2),
                'monthly_total': round(monthly_prediction, 2),
                'estimated_transactions': round(avg_transactions, 1)
            }
        
        return predictions
    
    def get_category_insights(self):
        """Get insights about spending patterns"""
        df = self.prepare_data()
        
        insights = {}
        for category in df['category'].unique():
            cat_data = df[df['category'] == category]
            
            insights[category] = {
                'avg_amount': round(cat_data['amount'].mean(), 2),
                'max_amount': round(cat_data['amount'].max(), 2),
                'min_amount': round(cat_data['amount'].min(), 2),
                'total_spent': round(cat_data['amount'].sum(), 2),
                'transaction_count': len(cat_data)
            }
        
        return insights

# Test
if __name__ == "__main__":
    predictor = ExpensePredictor()
    score = predictor.train_model()
    print(f"📈 Model R² Score: {score:.2f}")
    
    print("\n🔮 Next Month Predictions:")
    predictions = predictor.predict_next_month()
    for category, pred in predictions.items():
        print(f"{category}: ₹{pred['monthly_total']}")