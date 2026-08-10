{{ config(materialized='view')
}}

with low_ratings_list as (
select fhrs_id, row_number() over(partition by local_authority_code order by rating_score) as rn, business_name, postcode, local_authority_code, rating_score, rating_date 
from {{ ref('fact_hygiene_ratings')}}
where rating_score <= 2)

select fhrs_id, rn, local_authority_name,  business_name, rating_score, postcode, local_authority_code, rating_date from low_ratings_list join {{ ref('dim_local_authorities') }} dla using(local_authority_code)
