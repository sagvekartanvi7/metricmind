SELECT
    transaction_id,
    transaction_date,
    DATE_TRUNC('quarter', transaction_date) AS quarter,
    region,
    product,
    quantity,
    unit_price,
    revenue,
    cost,
    (revenue - cost) AS margin_amount,
    ROUND((revenue - cost) / NULLIF(revenue, 0), 4) AS margin_pct
FROM {{ ref('stg_transactions') }}