{{ config(
    materialized='view',
) }}

with latest_restaurant_status as (
    select 
        fhrs_id, 
        business_name, 
        postcode, 
        local_authority_code, 
        rating_score, 
        rating_date,
        updated_at,
        row_number() over(partition by fhrs_id order by updated_at desc) as latest_rn
    from {{ ref('fact_hygiene_ratings')}}
),

low_ratings_list as (
    select 
        fhrs_id, 
        business_name, 
        postcode, 
        local_authority_code, 
        rating_score, 
        rating_date,
        updated_at,
        row_number() over(partition by local_authority_code order by rating_score) as rn
    from latest_restaurant_status
    where latest_rn = 1         
      and rating_score <= 2      
)

select 
    l.fhrs_id, 
    l.rn, 
    dla.local_authority_name,  
    l.business_name, 
    l.rating_score, 
    l.postcode, 
    l.local_authority_code, 
    l.rating_date,
    l.updated_at
from low_ratings_list l
join {{ ref('dim_local_authorities') }} dla using(local_authority_code)
