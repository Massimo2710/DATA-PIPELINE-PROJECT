SELECT
    category,
    COUNT(DISTINCT purchase_id) AS total_purchases,
    SUM(quantity) AS total_items_sold,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_transaction_value
FROM {{ ref('fct_purchases') }}
GROUP BY category
ORDER BY total_revenue DESC