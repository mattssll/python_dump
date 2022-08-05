

  create or replace table `vectux-01`.`dwh_staging`.`st_rfm`
  
  
  OPTIONS()
  as (
    

WITH max_timestamp AS (
  SELECT 
    MAX(invoice_timestamp) AS max_timestamp
  FROM `vectux-01`.`source`.`rfm_ext_dbt_table` 
  WHERE customer is not null
), grouped_values AS (
  SELECT 
    customer_id, 
    MAX(invoice_timestamp) AS last_ordered_timestamp,
    DATE_DIFF(max(max_timestamp.max_timestamp), MAX(invoice_timestamp), DAY) AS abs_recency_days,
    COUNT(invoice_id) AS abs_count_freq,
    SUM(price) AS abs_sum_price
  FROM `vectux-01`.`source`.`rfm_ext_dbt_table` , max_timestamp
  WHERE customer is not null
  GROUP BY customer_id
)

SELECT 
    customer_id, 
    last_ordered_timestamp,
    date(last_ordered_timestamp) AS last_ordered_date,
    abs_recency_days,
    abs_count_freq,
    abs_sum_price,
    ntile(4) OVER (ORDER BY abs_recency_days) AS value_recency,
    ntile(4) OVER (ORDER BY abs_count_freq) AS value_frequency,
    ntile(4) OVER (ORDER BY abs_sum_price) AS value_monetary
  FROM grouped_values
  );
    