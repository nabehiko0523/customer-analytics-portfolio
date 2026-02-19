import duckdb

# Implement SQL inline
result = duckdb.sql("""
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(order_amount) as total_spent
    FROM 'data/sample_transactions.csv'
    GROUP BY customer_id
    ORDER BY total_spent DESC
    LIMIT 10
""").df()

print(result)