/*
LTV calculation for customer segmentation (Life Time Value)

Business purpose:
- Estimate the long-term value of customers
- Evaluate marketing ROI by comparing with CAC (Customer Acquisition Cost)

Points to consider:
- Calculate average purchase frequency, average purchase price, and customer lifespan
- Simple LTV = Average Purchase Value × Purchase Frequency × Customer Lifespan
*/

WITH customer_summary AS (
    SELECT
        customer_id,
        MIN(order_date) AS first_purchase_date,
        MAX(order_date) AS last_purchase_date,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(order_amount) AS total_revenue,
        AVG(order_amount) AS avg_order_value,
        DATEDIFF(day, MIN(order_date), MAX(order_date)) AS customer_lifespan_days
    FROM transactions
    GROUP BY customer_id
),

ltv_calculation AS (
    SELECT
        customer_id,
        first_purchase_date,
        last_purchase_date,
        total_orders,
        total_revenue,
        avg_order_value,
        customer_lifespan_days,
        
        -- Purchase frequency（orders per month）
        CASE
            WHEN customer_lifespan_days > 0 
            THEN total_orders / NULLIF(customer_lifespan_days / 30.0, 0)
            ELSE total_orders
        END AS purchase_frequency_monthly,
        
        -- Customer lifetime（months）
        GREATEST(customer_lifespan_days / 30.0, 1) AS customer_lifetime_months,
        
        -- Simple LTV calculation
        avg_order_value * total_orders AS historical_ltv,
        
        -- Estimted LTV for the next 12 months
        -- LTV = AOV × Purchase Frequency × Customer Lifetime
        avg_order_value * 
        (CASE
            WHEN customer_lifespan_days > 0 
            THEN total_orders / NULLIF(customer_lifespan_days / 30.0, 0)
            ELSE total_orders
        END) *
        12 AS predicted_ltv_12months  -- Estimati LTV for the next 12 months
        
    FROM customer_summary
)

SELECT
    -- Aggregate by LTV segment
    CASE
        WHEN predicted_ltv_12months >= 100000 THEN 'High Value'
        WHEN predicted_ltv_12months >= 50000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS ltv_segment,
    COUNT(*) AS customer_count,
    ROUND(AVG(total_orders), 1) AS avg_orders,
    ROUND(AVG(avg_order_value), 0) AS avg_order_value,
    ROUND(AVG(purchase_frequency_monthly), 2) AS avg_monthly_frequency,
    ROUND(AVG(historical_ltv), 0) AS avg_historical_ltv,
    ROUND(AVG(predicted_ltv_12months), 0) AS avg_predicted_ltv,
    ROUND(SUM(predicted_ltv_12months), 0) AS total_predicted_value
FROM ltv_calculation
GROUP BY 
    CASE
        WHEN predicted_ltv_12months >= 100000 THEN 'High Value'
        WHEN predicted_ltv_12months >= 50000 THEN 'Medium Value'
        ELSE 'Low Value'
    END
ORDER BY avg_predicted_ltv DESC;

-- In case you want to see individual customer LTV predictions, you can run the following query:
-- SELECT * FROM ltv_calculation ORDER BY predicted_ltv_12months DESC LIMIT 100;