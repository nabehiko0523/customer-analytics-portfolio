import pandas as pd
import numpy as np
from datetime import datetime

# Load the dataset
df = pd.read_csv('data/sample_transactions.csv')
df['order_date'] = pd.to_datetime(df['order_date'])

#1. Identify the first purchase date for each customer
first_purchase = df.groupby('customer_id')['order_date'].min().reset_index()
first_purchase.columns = ['customer_id', 'cohort_month']
first_purchase['cohort_month'] = first_purchase['cohort_month'].dt.to_period('M')

#2. Merge the cohort information back to the original dataset
df['order_month'] = df['order_date'].dt.to_period('M')
df = df.merge(first_purchase, on='customer_id', how='left')

#3. Calculate the cohort index (number of months since the first purchase)
df['month_since_first'] = (df['order_month'] - df['cohort_month']).apply(lambda x: x.n)

#4. Number of unique customers in each cohort
cohort_data = df.groupby(['cohort_month', 'month_since_first'])['customer_id'].nunique().reset_index()
cohort_data.columns = ['cohort_month', 'month_since_first', 'active_customers']

#5. Cohort size (number of unique customers in the first month)
cohort_sizes = first_purchase.groupby('cohort_month')['customer_id'].nunique().reset_index()
cohort_sizes.columns = ['cohort_month', 'cohort_customers']

#6. Calulate retention rate
cohort_data = cohort_data.merge(cohort_sizes, on='cohort_month', how='left')
cohort_data['retention_rate'] = (cohort_data['active_customers'] / cohort_data['cohort_customers'] * 100).round(2)

#7. Pivot the data for better visualization
cohort_pivot = cohort_data.pivot_table(
    index='cohort_month',
    columns='month_since_first',
    values='retention_rate',
    fill_value=0
)

#8 . Display the cohort analysis results
print("=" * 100)
print("Cohort RetentionAnalysis")
print("=" * 100)
print("\nRetention Rate by Cohort (%):\n")
print(cohort_pivot.to_string())

#9. Summary statistics
print("\n" + "=" * 100)
print("Summary Statistics")
print("=" * 100)

for month in [1, 3, 6, 12]:
    if month in cohort_pivot.columns:
        avg_retention = cohort_pivot[month].mean()
        print(f"Average {month}-month retention: {avg_retention:.2f}%")

#10. Cohort with the highest retention at 3 months
print("\n" + "=" * 100)
print("Top Performing Cohorts")
print("=" * 100)

# ranking cohorts based on 3-month retention
if 3 in cohort_pivot.columns:
    top_cohorts = cohort_pivot[3].sort_values(ascending=False).head(5)
    print("\nTop 5 Cohorts by 3-Month Retention:")
    for cohort, retention in top_cohorts.items():
        print(f" {cohort}: {retention:.2f}%")

#11. Store the cohort analysis results in a CSV file
cohort_data.to_csv('data/cohort_retention_analysis_results.csv', index=False)
cohort_pivot.to_csv('data/cohort_retention_pivot.csv')

print("\n" + "=" * 100)
print("✓ Results saved to:")
print("  - data/cohort_retention_results.csv (detailed)")
print("  - data/cohort_retention_pivot.csv (pivot table)")
print("=" * 100)