SELECT
    transaction_id,
    transaction_date,
    region,
    product,
    quantity,
    unit_price,
    revenue,
    cost
FROM {{ source('raw', 'transactions_raw') }}