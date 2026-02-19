import pandas as pd
import numpy as np
from datetime import datetime

# Load the dataset
df = pd.read_csv('data/sample_transactions.csv')
df['order_date'] = pd.to_datetime(df['order_date'])

current_date = datetime.now()

# 1. Calculate customer-level metrics
customer_summary = df.groupby('customer_id').agg({
    'order_date': ['min', 'max'],
    'order_id': 'nunique',
    'order_amount': ['sum', 'mean']
}).reset_index()

customer_summary.columns = ['customer_id', 'first_purchase', 'last_purchase', 
                            'total_orders', 'total_revenue', 'avg_order_value']

# 2. Customer lifespan calculation
customer_summary['lifespan_days'] = (customer_summary['last_purchase'] - customer_summary['first_purchase']).dt.days
customer_summary['lifespan_months'] = customer_summary['lifespan_days'] / 30.0
customer_summary['lifespan_months'] = customer_summary['lifespan_months'].apply(lambda x: max(x, 1))

# 3. Purchase frequency (orders per month)
customer_summary['purchase_frequency'] = customer_summary.apply(
    lambda row: row['total_orders'] / row['lifespan_months'] if row['lifespan_days'] > 30 else row['total_orders'],
    axis=1
)

# 4. LTV計算
customer_summary['historical_ltv'] = customer_summary['total_revenue']
customer_summary['predicted_ltv_12m'] = (
    customer_summary['avg_order_value'] * 
    customer_summary['purchase_frequency'] * 
    12
)
customer_summary['predicted_ltv_24m'] = (
    customer_summary['avg_order_value'] * 
    customer_summary['purchase_frequency'] * 
    24
)

# 5. Days since last purchase
customer_summary['days_since_last'] = (current_date - customer_summary['last_purchase']).dt.days

# 6. LTV segmentation
def classify_ltv_segment(ltv):
    if ltv >= 100000:
        return 'Platinum'
    elif ltv >= 50000:
        return 'Gold'
    elif ltv >= 20000:
        return 'Silver'
    else:
        return 'Bronze'

customer_summary['ltv_segment'] = customer_summary['predicted_ltv_12m'].apply(classify_ltv_segment)

# 7. Churn risk assessment
def assess_churn_risk(days):
    if days > 180:
        return 'High Risk'
    elif days > 90:
        return 'Medium Risk'
    else:
        return 'Active'

customer_summary['churn_risk'] = customer_summary['days_since_last'].apply(assess_churn_risk)

# 8. Summarize by LTV segment
segment_summary = customer_summary.groupby('ltv_segment').agg({
    'customer_id': 'count',
    'total_orders': 'mean',
    'avg_order_value': 'mean',
    'purchase_frequency': 'mean',
    'lifespan_months': 'mean',
    'historical_ltv': 'mean',
    'predicted_ltv_12m': ['mean', 'sum'],
    'days_since_last': 'mean'
}).round(2)

segment_summary.columns = ['customer_count', 'avg_orders', 'avg_order_value', 
                           'avg_frequency', 'avg_lifetime_months', 'avg_historical_ltv',
                           'avg_predicted_ltv_12m', 'total_predicted_value', 'avg_days_since_last']

# Segment percentage
segment_summary['segment_pct'] = (segment_summary['customer_count'] / segment_summary['customer_count'].sum() * 100).round(2)

# Sort by predicted LTV
segment_summary = segment_summary.sort_values('avg_predicted_ltv_12m', ascending=False)

# 9. Display results
print("=" * 100)
print("CUSTOMER LIFETIME VALUE (LTV) ANALYSIS")
print("=" * 100)
print("\nSegment Summary:\n")
print(segment_summary.to_string())

# 10. Top customers list
print("\n" + "=" * 100)
print("TOP 10 CUSTOMERS BY PREDICTED LTV (12 months)")
print("=" * 100)
top_customers = customer_summary.nlargest(10, 'predicted_ltv_12m')[
    ['customer_id', 'total_orders', 'total_revenue', 'predicted_ltv_12m', 'ltv_segment', 'churn_risk']
]
print(top_customers.to_string(index=False))

# 11. Churn risk analysis
print("\n" + "=" * 100)
print("CHURN RISK ANALYSIS")
print("=" * 100)
churn_analysis = customer_summary.groupby(['ltv_segment', 'churn_risk']).size().unstack(fill_value=0)
print(churn_analysis)

# 12. Total predicted value
total_12m = customer_summary['predicted_ltv_12m'].sum()
total_24m = customer_summary['predicted_ltv_24m'].sum()

print("\n" + "=" * 100)
print("TOTAL PREDICTED VALUE")
print("=" * 100)
print(f"12-Month Total LTV: ¥{total_12m:,.0f}")
print(f"24-Month Total LTV: ¥{total_24m:,.0f}")
print(f"Average LTV per Customer (12m): ¥{total_12m/len(customer_summary):,.0f}")

# 13. Store results in CSV files
customer_summary.to_csv('data/ltv_analysis_results.csv', index=False)
segment_summary.to_csv('data/ltv_segment_summary.csv')

print("\n" + "=" * 100)
print("✓ Results saved to:")
print("  - data/ltv_analysis_results.csv (detailed)")
print("  - data/ltv_segment_summary.csv (summary)")
print("=" * 100)