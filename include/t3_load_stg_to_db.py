import os
from dotenv import load_dotenv
from datetime import datetime
from include.constants import LOCAL_AUTHORITY_CODE
from include.t3_xml_parsing import parse_xml
import psycopg

load_dotenv()

def load_to_db():
    print("db staging table 업로드 시작")
    today_date = datetime.now().date()
    code_list = LOCAL_AUTHORITY_CODE

    DB_CONFIG = {
        "host": os.environ.get("DB_HOST"), 
        "port": 6543,  
        "dbname": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
    }

    # stg 테이블에 벌크 인서트
    insert_query = """ 
        INSERT INTO stg_fhrs_ratings (
            FHRSID, BusinessName, PostCode, RatingValue, RatingDate, LocalAuthorityCode, LocalAuthorityName
        ) 
        VALUES (
            %(FHRSID)s, %(BusinessName)s, %(PostCode)s, %(RatingValue)s, %(RatingDate)s, %(LocalAuthorityCode)s, %(LocalAuthorityName)s
        );
    """

    try:
        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                # 테이블이 없다면 임시 생성
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS stg_fhrs_ratings (
                        FHRSID VARCHAR(50) PRIMARY KEY,
                        BusinessName VARCHAR(255),
                        PostCode VARCHAR(50),
                        RatingValue VARCHAR(50),
                        RatingDate DATE,
                        LocalAuthorityCode VARCHAR(50),
                        LocalAuthorityName VARCHAR(255),
                        updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                # staging 테이블 초기화
                cur.execute("TRUNCATE TABLE stg_fhrs_ratings;")
                total_inserted_rows = 0
                # 벌크 인서트 실행
                # 커넥션 안에서 33개 보로우 루프 돌기
                for code in code_list:
                    production_path_name = (
                        f"/opt/airflow/data/{today_date}/fhrs-{code}-{today_date}.xml"
                    )
                    # local_path_name = f"./data/{today_date}/fhrs-{code}-{today_date}.xml"

                    # 파일이 존재하지 않는 경우를 대비한 방어 코드
                    if not os.path.exists(production_path_name):
                        print(
                            f"[스킵] 파일이 존재하지 않습니다: {production_path_name}"
                        )
                        continue

                    print(f"[처리 중] 보로우 코드 {code} 파일 파싱 시작...")
                    parsed_xml_data = parse_xml(production_path_name)

                    if not parsed_xml_data:
                        print(f"[안내] 보로우 코드 {code}에 적재할 데이터가 없습니다.")
                        continue

                    # 해당 보로우 데이터 벌크 인서트 실행
                    cur.executemany(insert_query, parsed_xml_data)
                    total_inserted_rows += len(parsed_xml_data)
                    print(f"성공: {len(parsed_xml_data)}개 행 적재 완료.")

                # 루프가 다 끝나면 모든 보로우 데이터를 한 번에 커밋
                conn.commit()
                print(
                    f"[완료] 전체 보로우 적재가 끝났습니다. 총 {total_inserted_rows}개 행 반영."
                )

    except Exception as e:
        print(f"에러 발생: {e}")

