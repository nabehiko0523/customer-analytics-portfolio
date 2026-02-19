"""
DuckDB implementation of RFM analysis
File: scripts/run_rfm_duckdb.py
"""

import duckdb
import pandas as pd
import os
import sys

def main():
    # ファイル存在確認
    csv_path = 'data/sample_transactions.csv'
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found")
        print("Run: python scripts/generate_sample_data.py")
        sys.exit(1)
    
    print("=" * 80)
    print("DuckDB RFM Analysis")
    print("=" * 80)
    
    # DuckDB接続
    print("\n1. Connecting to DuckDB...")
    con = duckdb.connect(':memory:')
    print("   ✓ Connected")
    
    # データロード
    print("\n2. Loading data...")
    con.execute(f"""
        CREATE TABLE transactions AS 
        SELECT * FROM read_csv_auto('{csv_path}')
    """)
    
    row_count = con.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    print(f"   ✓ Loaded {row_count} transactions")
    
    # RFM分析SQL
    print("\n3. Running RFM analysis...")
    
    rfm_sql = """
    WITH customer_metrics AS (
        SELECT
            customer_id,
            MAX(CAST(order_date AS DATE)) AS last_order_date,
            COUNT(DISTINCT order_id) AS frequency,
            SUM(order_amount) AS monetary,
            AVG(order_amount) AS avg_order_value
        FROM transactions
        GROUP BY customer_id
    ),
    
    rfm_calculation AS (
        SELECT
            customer_id,
            last_order_date,
            DATE_DIFF('day', last_order_date, CURRENT_DATE) AS recency_days,
            frequency,
            monetary,
            avg_order_value,
            NTILE(5) OVER (ORDER BY DATE_DIFF('day', last_order_date, CURRENT_DATE) DESC) AS r_score,
            NTILE(5) OVER (ORDER BY frequency) AS f_score,
            NTILE(5) OVER (ORDER BY monetary) AS m_score
        FROM customer_metrics
    ),
    
    customer_segmentation AS (
        SELECT
            *,
            r_score + f_score + m_score AS rfm_total,
            CASE
                WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
                WHEN r_score >= 3 AND f_score >= 4 THEN 'Loyal Customers'
                WHEN r_score >= 4 AND f_score <= 2 THEN 'Promising'
                WHEN r_score >= 3 AND m_score >= 4 THEN 'Big Spenders'
                WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
                WHEN r_score <= 2 AND m_score >= 4 THEN 'Cant Lose Them'
                WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost'
                ELSE 'Need Attention'
            END AS customer_segment
        FROM rfm_calculation
    )
    
    SELECT
        customer_segment,
        COUNT(*) AS customer_count,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS segment_pct,
        ROUND(AVG(recency_days), 1) AS avg_recency_days,
        ROUND(AVG(frequency), 1) AS avg_frequency,
        ROUND(AVG(monetary), 0) AS avg_monetary,
        ROUND(AVG(avg_order_value), 0) AS avg_order_value
    FROM customer_segmentation
    GROUP BY customer_segment
    ORDER BY avg_monetary DESC
    """
    
    # クエリ実行
    result = con.execute(rfm_sql).fetchdf()
    print("   ✓ Analysis complete")
    
    # 結果表示
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print("\n" + result.to_string(index=False))
    
    # 保存
    output_path = 'data/rfm_duckdb_results.csv'
    result.to_csv(output_path, index=False)
    print(f"\n✓ Saved to: {output_path}")
    
    # クリーンアップ
    con.close()
    
    print("\n" + "=" * 80)
    print("Complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()