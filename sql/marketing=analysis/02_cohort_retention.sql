/*
cohort retention analysis

Business purpose:
- Track the retention of customers over time based on their first purchase date
- Itendify the effectiveness of marketing campaings or service improvements. 

Points to consider:
- Define cohort based on the month of the first purchase
- Calculate retention rate for each cohort over subsequent months
- Easier visualization by pivot table. 
*/

WITH first_purchase AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) AS cohort_month
    FROM transactions
    GROUP BY customer_id
),

customer_activity AS (
    SELECT DISTINCT
        t.customer_id,
        fp.cohort_month,
        DATE_TRUNC('month', t.order_date) AS activity_month,
        DATEDIFF(month, fp.cohort_month, DATE_TRUNC('month', t.order_date)) AS month_since_first
    FROM transactions t
    INNER JOIN first_purchase fp ON fp.customer_id = t.customer_id
),

cohort_size AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_customers
    FROM first_purchase
    GROUP BY cohort_month
),

retention_table AS (
    SELECT
        ca.cohort_month,
        ca.month_since_first,
        COUNT(DISTINCT ca.customer_id) AS active_customers
        cs.cohort_customers,
        ROUND(COUNT(DISTINCT ca.customer_id) * 100.0 / cs.cohort_customers, 2) AS retention_rate
    FROM customer_activity ca
    INNER JOIN cohort_size cs ON cs.cohort_month = ca.cohort_month
    GROUP BY ca.cohort_month, ca.month_since_first, cs.cohort_customers
)

SELECT
    cohort_month,
    cohort_customers,
    month_since_first,
    active_customers,
    retention_rate
FROM retention_table
WHERE month_since_first <= 12
ORDER BY cohort_month, month_since_first;