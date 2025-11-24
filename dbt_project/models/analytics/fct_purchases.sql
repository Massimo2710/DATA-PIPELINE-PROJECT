SELECT
    p.purchase_id,
    p.user_id,
    p.product_id,
    p.quantity,
    p.purchase_date,
    prod.price,
    p.quantity * prod.price AS total_amount,
    prod.category,
    prod.product_name
FROM {{ ref('stg_purchases') }} p
LEFT JOIN {{ ref('stg_products') }} prod 
    ON p.product_id = prod.product_id