{{ config ( 
  materialized="table",
  schema="dwh"
  )
}}

SELECT 
    customer_id,
    tenant,
    last_ordered_timestamp,
    abs_recency_days,
    abs_count_freq,
    abs_sum_price,
    value_recency,
    value_frequency,
    value_monetary,
    value_recency || value_frequency || value_monetary AS rfm_concat,
    (value_recency+value_frequency+value_monetary) AS rfm_final,
    CASE 
      WHEN (value_recency+value_frequency+value_monetary) >= 9 THEN 'Can\'t Lose Them'
      WHEN (value_recency+value_frequency+value_monetary) >= 8 THEN 'Champions'
      WHEN (value_recency+value_frequency+value_monetary) >= 7 THEN 'Loyal'
      WHEN (value_recency+value_frequency+value_monetary) >= 6 THEN 'Has Potential'
      WHEN (value_recency+value_frequency+value_monetary) >= 5 THEN 'Promising'
      WHEN (value_recency+value_frequency+value_monetary) >= 4 THEN 'Needs Atention'
      ELSE 'Requires Activation'
    END AS rfm_category
FROM {{ ref('st_rfm') }}