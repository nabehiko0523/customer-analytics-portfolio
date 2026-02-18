import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# setting seed for reproducibility
np.random.seed(42)

# Generate sample customer data
n_customers = 100
n_orders = 500

cusotmer_ids = [f"CUST{str(i).zfill(3)}" for i in range(1, n_customers + 1)]

# Generate orders
orders = []
start_date = datetime(2025, 1, 1)

for i in range(n_orders):
    cusotmer_id = np.random.choice(cusotmer_ids)
    order_id = f'0{str(i+1).zfill(4)}'

    # Random order date within the last 12 months
    days_ago = np.random.randint(0, 365)
    order_date = start_date + timedelta(days=days_ago)

    # Random order amount
    order_amount = int(np.random.lognormal(9, 0.8))

    # Random product category
    categories = ['Electronics', 'Clothing', 'Books', 'Food', 'Sports']
    product_category = np.random.choice(categories)

    orders.append({
        'order_id': order_id,
        'customer_id': cusotmer_id,
        'order_date': order_date.strftime('%Y-%m-%d'),
        'order_amount': order_amount,
        'product_category': product_category
    })

df = pd.DataFrame(orders)
df = df.sort_values('order_date')
df.to_csv('data/sample_transactions.csv', index=False)

print(f"Generated {len(df)} orders for {df['customer_id'].nunique()} customers.")
print(f"Date range': {df['order_date'].min()} to {df['order_date'].max()}")
print(f"\nSample:\n{df.head(10)}")