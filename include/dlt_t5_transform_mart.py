3. 데이터 마트: 미리 계산된 데이터. 운영팀은 간단한 쿼리나 BI 툴에 연결해서 바로 업무에 사용한다.


Task 4 (변환 및 마트): Staging ➔ Dim ➔ Fact ➔ Mart 과정을 하나의 SQL 스크립트나 하나의 태스크 안에서 순서대로 쭉 실행

1. 보로우별 2점 이하인 식당의 비율 (33 rows)
"""

WITH fhrs_summary AS (
    SELECT 
        local_authority_code,
        COUNT(CASE WHEN rating_score <= 2 THEN 1 END) AS below_2_cnt,
        COUNT(*) AS total_cnt
    FROM fact_hygiene_ratings 
    GROUP BY local_authority_code
) 
SELECT 
    f.local_authority_code, 
    dim.local_authority_name, 
    f.below_2_cnt, 
    f.total_cnt,
    ROUND(f.below_2_cnt * 100.0 / f.total_cnt, 2) AS ratio
FROM fhrs_summary f
JOIN dim_local_authorities dim USING (local_authority_code)
ORDER BY ratio DESC;

"""

2. 보로우별 2점 이하 식당 리스트 
"""
with ratings as (
select fhrs_id, row_number() over(partition by local_authority_code) as rn, business_name, post_code, local_authority_code, rating_score, rating_date 
from fact_hygiene_ratings
where rating_score <=2)

select fhrs_id, rn, local_authority_name,  business_name, rating_score, post_code, local_authority_code, rating_date from ratings join dim_local_authorities dla using(local_authority_code)
"""


3. 
models/rpt_fhrs_downgraded_low_rating_list.sql
과거 정상 등급(3점 이상)에서 이번에 새롭게 2점 이하로 떨어진 위생 불량 식당 목록