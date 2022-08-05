

WITH rfm_values AS (
  SELECT 
      customer_id, 
      last_ordered_timestamp,
      abs_recency_days,
      abs_count_freq,
      abs_sum_price,
      ntile(4) OVER (ORDER BY abs_recency_days) AS value_recency,
      ntile(4) OVER (ORDER BY abs_count_freq) AS value_frequency,
      ntile(4) OVER (ORDER BY abs_sum_price) AS value_monetary
  FROM `vectux-01`.`dwh_staging`.`st_rfm`
) 

SELECT 
    customer_id,
    last_ordered_timestamp,
    value_recency,
    value_frequency,
    value_monetary,
    value_recency || value_frequency || value_monetary AS rfm_concat,
    (value_recency+value_frequency+value_monetary) AS rfm_final,
    CASE 
      WHEN (value_recency+value_frequency+value_monetary) >= 10 THEN 'awesome'
      WHEN (value_recency+value_frequency+value_monetary) >= 7 THEN 'good'
      WHEN (value_recency+value_frequency+value_monetary) >= 7 THEN 'bad'
      ELSE 'horrible'
    END AS rfm_category
FROM rfm_values