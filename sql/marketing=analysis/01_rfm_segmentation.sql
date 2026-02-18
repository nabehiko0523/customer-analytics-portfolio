/*
Customer segmentation by RFM (Recency, Frequency, Monetary)

Business purpose:
- Assess customers based on their 1. Recency 2. Frequency 3. Monetary value
- Identify marketing strategy by segmentation

Points to consider:
- NTILE function to score customers into 5 groups (1-5)
- CASE sentence to assign segment labels based on RFM scores
- Define segments actually used in a practical marketing strategy
*/

WITH cusotmer_metrics AS (
    SELECT
        customer_id, 
        MAX(order_date) AS last_purchase_date,
        COUNT(DISTINCT order_id) AS frequency,
        SUM(order_amount) AS monetary,
        AVG(order_amount) AS avg_order_value,
    FROM transactions
    WHERE order_date >= DATEADD(year, -1, CURRENT_DATE)
    GROUP BY customer_id
),

rfm_calculation AS (
    SELECT
        customer_id,
        last_order_date,
        DATADIFF(day, last_order_date, CURRENT_DATE) AS recency_days,
        frequency,
        monetary,
        avg_order_value,
        NTILE(5) OVER (ORDER BY DATEDIFF(day, last_order_date, DATEADD(year, -1, CURRENT_DATE)) DESC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
    FROM cusomter_metrics
),

cusomter_segmentation AS (
    SELECT
        *,
        r_score + f_score + m_score AS rfm_total,
        CASE 
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
            WHEN r_score >= 3 AND f_score >= 4 THEN 'Loyal Customers'
            WHEN r_score >= 4 AND f_score >= 2 THEN 'Promising'
            WHEN r_score >= 3 AND m_score >= 4 THEN 'Big Spenders'
            WHEN r_score >= 3 AND f_score <= 2 AND m_score >= 2 THEN 'Need Attention'
            WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
            WHEN r_score <= 2 AND m_score >= 4 THEN 'Cant Lose Them'
            WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost'
            ELSE 'Others'
        END AS Customer_segment,
        -- Define marketing strategy based on segment
        CASE
            WHEN r_score >= 4 AND f_score >= 4 THEN 'VIP treatment, exclusie offers'
            WHEN r_score >= 4 AND f_score >= 2 THEN 'Onboarding, engagement campaigns'
            WHEN r_score <= 2 AND f_score >= 3 THEN 'Win-back campaigns, special discounts'
            WHEN r_score <= 2 AND f_score <= 2 THEN 'Re-engagement campaigns, surveys'
            ELSE 'Standard retention'
        END AS recommended_action
    FROM rfm_calculation
)

SELECT
    customer_segment,
    COUNT(*) AS customer_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS segment_pct,
    ROUND(AVG(recency_days), 1) AS avg_revency_days,
    ROUND(AVG(frequency), 1) AS avg_frequency,
    ROUND(AVG(monetary), 1) AS avg_monetary,
    ROUND(ACG(avg_order_value), 0) AS avg_order_value
FROM cusomter_segmentation
GROUP BY customer_segment
ORDER BY avg_monetary DESC;