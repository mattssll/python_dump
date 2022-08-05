{{ config ( 
  materialized="table",
  schema="dwh_staging"
  )
}}

-- get max_timestamp to calculate recency
WITH max_timestamp AS (
  SELECT
    customer,
    MAX(invoice_timestamp) AS max_timestamp
  FROM {{ ref('st_transactions_rfm') }}
  WHERE customer IS NOT NULL 
  GROUP BY customer
), grouped_rfm_by_customer_id AS (
  SELECT 
    customer_id, 
    MAX(invoice_timestamp) AS last_ordered_timestamp,
    DATE_DIFF(max(max_timestamp.max_timestamp), MAX(invoice_timestamp), DAY) AS abs_recency_days,
    COUNT(invoice_id) AS abs_count_freq,
    SUM(price) AS abs_sum_price,
    MAX(t1.customer) AS tenant
  FROM {{ ref('st_transactions_rfm') }} t1 , max_timestamp
  LEFT JOIN max_timestamp t2 
    ON t1.customer = max_timestamp.customer
  WHERE t1.customer IS NOT NULL
  GROUP BY customer_id
)

SELECT 
    customer_id,
    tenant, 
    last_ordered_timestamp,
    DATE(last_ordered_timestamp) AS last_ordered_date,
    abs_recency_days,
    abs_count_freq,
    abs_sum_price,
    NTILE(4) OVER (ORDER BY abs_recency_days) AS value_recency,
    NTILE(4) OVER (ORDER BY abs_count_freq) AS value_frequency,
    NTILE(4) OVER (ORDER BY abs_sum_price) AS value_monetary
FROM grouped_rfm_by_customer_id