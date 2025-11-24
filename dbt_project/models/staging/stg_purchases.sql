SELECT
    purchase_id,
    user_id,
    product_id,
    quantity,
    purchase_date
FROM {{ source('raw', 'purchases') }}