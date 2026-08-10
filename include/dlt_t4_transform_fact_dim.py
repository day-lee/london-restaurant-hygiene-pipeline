
def transform_fact_dim():

0. psycopg로 SQL 명령 던져서 postgresql엔진이 처리하게 만든다.
"""
2. 파이썬 & psycopg 단계커넥션 열기: 
psycopg를 이용해 Docker PostgreSQL 컨테이너에 연결(Connection)하고 커서(Cursor)를 생성합니다.
로직 이식: 디비버에서 성공했던 그 로우(Raw) SQL 쿼리 문자열을 그대로 파이썬 변수(예: query = """...""")에 할당합니다.
실행 및 커밋: cursor.execute(query)로 디비에 명령을 던진 후, 반드시 connection.commit()을 수행하여 DB에 최종 반영합니다.자원 닫기: 작업이 끝나면 커서와 커넥션을 닫아줍니다(close()).
"""


1. dim 차원 데이터 먼저 만든다.
-> Fact 에서 local_authority_code를 FK로 연결할 수 있도록 
"""
맨 처음에는 테이블 만들어 줘야함. 
CREATE TABLE IF NOT EXISTS dim_local_authorities (
    local_authority_code VARCHAR(50) PRIMARY KEY,
    local_authority_name VARCHAR(50),
    dw_inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

SCD 의 경우 덮어쓰기 전략 

INSERT INTO dim_local_authorities (local_authority_code, local_authority_name)
SELECT localauthoritycode, localauthorityname
FROM public.stg_fhrs_ratings
GROUP BY localauthoritycode, localauthorityname
ON CONFLICT (local_authority_code) 
DO UPDATE SET 
    local_authority_name = EXCLUDED.local_authority_name,
    dw_inserted_at = CURRENT_TIMESTAMP;

"""

2. 팩트 테이블 만든다.

    1.staging과 dim 테이블을 조인해서 FK로 연결되게 만든다. 
    2. mixed type data 처리: rating_value와 ratinv_score 로 컬럼을 나눠준다. 

rating_value (VARCHAR): 원본 그대로 저장 - 참고용
rating_score (INT): 숫자로 변환 가능한 값만 변환하여 저장하고, 문자열인 경우는 NULL 처리 (예: 5, NULL, NULL) - 계산용

이 방식의 데이터 흐름 (Staging ➔ Fact)데이터를 팩트 테이블에 집어넣을 때, SQL의 CASE WHEN 문이나 REGEXP_LIKE 같은 정규식을 이용해 판단합니다.
값이 0~5 사이의 숫자 형태라면 rating_score에 정수로 밀어 넣고, 숫자가 아닌 문자가 들어오면 NULL로 비워둡니다.

"""
맨 처음에는 테이블 만들어져야함 
CREATE TABLE IF NOT EXISTS fact_hygiene_ratings (
    fact_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- 자동 증가 PK
    fhrs_id VARCHAR(50),
    local_authority_code VARCHAR(50), 
    business_name VARCHAR(255),       
    post_code VARCHAR(50),
    rating_value VARCHAR(50),   -- 문자열(Exempt 등) 대비
    rating_score INTEGER,   
    rating_date DATE,
    dw_inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO fact_hygiene_ratings (
    fhrs_id,
    local_authority_code, 
    business_name,       
    post_code,
    rating_value,   
    rating_score,   
    rating_date
)
SELECT 
    stg.fhrsid, 
    dim.local_authority_code, -- stg 대신 검증된 dim 테이블의 코드를 가져옴 (INNER JOIN을 통해 유령 코드 필터링)
    stg.businessname, 
    stg.postcode,
    stg.ratingvalue, 
    (CASE 
        WHEN stg.ratingvalue ~ '^[0-9]+$' THEN CAST(stg.ratingvalue AS INTEGER) 
        ELSE NULL 
    end) rating_score, -- 숫자인 경우에만 정수로 형변환하여 적재
    stg.ratingdate 
FROM public.stg_fhrs_ratings stg
INNER JOIN public.dim_local_authorities dim 
    ON stg.localauthoritycode = dim.local_authority_code;

"""
