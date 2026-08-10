{{ config(
    materialized='incremental',
    unique_key=['fhrs_id', 'updated_at'],
    incremental_strategy='append'
) }}

WITH source_data AS(SELECT 
    FHRSID AS fhrs_id, 
    LocalAuthorityCode AS local_authority_code,
    LocalAuthorityName AS local_authority_name,
    BusinessName AS business_name, 
    PostCode AS postcode,
    RatingValue AS rating_value, 
    (CASE 
        WHEN RatingValue ~ '^[0-9]+$' THEN CAST(RatingValue AS INTEGER) 
        ELSE NULL 
    end) rating_score, 
    RatingDate AS rating_date,
    updated_at AS src_updated_at
FROM public.stg_fhrs_ratings)
{% if is_incremental() %}
, latest_existing_rating AS (
    SELECT 
        fhrs_id,
        rating_score as last_rating    
    FROM (
        SELECT
       fhrs_id,
       rating_score,
       ROW_NUMBER() OVER(PARTITION BY fhrs_id ORDER BY updated_at DESC) as rn
    FROM {{ this }} 
) AS t
WHERE rn = 1
)
{% endif %}

SELECT 
    CAST(CONCAT(s.fhrs_id, TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD')) AS BIGINT) AS fact_key,
    s.fhrs_id, 
    s.local_authority_code,
    s.local_authority_name,
    s.business_name, 
    s.postcode,
    s.rating_value, 
    s.rating_score, 
    s.rating_date,
    CURRENT_TIMESTAMP AS updated_at
FROM source_data s

{% if is_incremental() %}
LEFT JOIN latest_existing_rating e ON s.fhrs_id = e.fhrs_id 
WHERE e.fhrs_id IS NULL OR s.rating_score != e.last_rating 
{% endif %}
