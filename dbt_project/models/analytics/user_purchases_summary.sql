SELECT
    u.user_id,
    u.name,
    u.email,
    u.country,
    COUNT(DISTINCT f.purchase_id) AS total_purchases,
    SUM(f.quantity) AS total_items_bought,
    ROUND(SUM(f.total_amount), 2) AS total_spent,
    ROUND(AVG(f.total_amount), 2) AS avg_purchase_amount
FROM {{ ref('stg_users') }} u
LEFT JOIN {{ ref('fct_purchases') }} f 
    ON u.user_id = f.user_id
GROUP BY u.user_id, u.name, u.email, u.country
ORDER BY total_spent DESC