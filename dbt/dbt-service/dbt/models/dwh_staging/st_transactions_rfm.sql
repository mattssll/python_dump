{{ config ( 
  materialized="table",
  schema="dwh_staging"
  )
}}
        
SELECT 
    CAST(customer_id AS STRING) || '_' || CAST(customer AS STRING) AS customer_id,
    invoice_id,
    invoice_timestamp,
    price,
    country_id,
    customer
FROM {{ source('source', 'rfm_ext_dbt_table') }}
WHERE customer IS NOT NULL  -- getting all tenants here

