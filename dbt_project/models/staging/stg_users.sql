SELECT
    user_id,
    name,
    email,
    country,
    created_at
FROM {{ source('raw', 'users') }}