{{ config(
    materialized='incremental',
    unique_key='local_authority_code'
) }}

SELECT
    localauthoritycode AS local_authority_code,
    localauthorityname AS local_authority_name,
    CURRENT_TIMESTAMP AS updated_at
FROM public.stg_fhrs_ratings 

GROUP BY localauthoritycode, localauthorityname


