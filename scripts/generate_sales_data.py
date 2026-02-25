import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# Generate synthetic sales data for 3 years (36 months)
start_date = datetime(2023, 1, 1)
months = 36

dates = [start_date + timedelta(days=30*i) for i in range(months)]

# Trend + Seasonality + Noise
trend = np.linspace(100000, 150000, months)
seasonality = 20000 * np.sin(np.linspace(0, 6*np.pi, months))
noise = np.random.normal(0, 5000, months)

sales = trend + seasonality + noise

# Product categories
categories = ['Electronics', 'Clothing', 'Books', 'Food', 'Sports']
data = []

for i, date in enumerate(dates):
    for category in categories:
        category_sales = sales[i] * (0.15 + 0.2 * categories.index(category) / len(categories))
        category_sales += np.random.normal(0, category_sales * 0.1)
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'category': category,
            'sales_amount': int(category_sales),
            'units_sold': int(category_sales / np.random.uniform(1000, 5000))
        })

df = pd.DataFrame(data)
df.to_csv('data/sales_history.csv', index=False)

print(f"✓ Generated {len(df)} records")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print("\nSample:")
print(df.head(10))