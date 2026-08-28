{{ config(
    materialized='view',
) }}

WITH fhrs_summary AS (
    SELECT 
        local_authority_code,
        MAX(updated_at) AS updated_at,
        COUNT(CASE WHEN rating_score <= 2 THEN 1 END) AS below_2_cnt,
        COUNT(*) AS total_cnt
    FROM {{ ref('fact_hygiene_ratings') }} 
    GROUP BY local_authority_code
) 
SELECT 
    f.local_authority_code, 
    dim.local_authority_name, 
    f.below_2_cnt, 
    f.total_cnt,
    ROUND(f.below_2_cnt * 100.0 / f.total_cnt, 2) AS ratio,
    f.updated_at
FROM fhrs_summary f
JOIN {{ ref('dim_local_authorities') }} dim USING (local_authority_code)
ORDER BY ratio DESC