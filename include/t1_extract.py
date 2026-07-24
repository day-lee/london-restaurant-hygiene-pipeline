### Milestone 1: Task 1 (Extract) – API ➔ Local `/tmp`
from datetime import datetime 
import requests

LOCAL_AUTHORITY_CODE = ['501', '502', '503', '504', '505', '506', '507', '508', '509', '510', '511', '512', '513', '514', '515', '516', '517', '518', '519', '520', '521', '522', '523', '524', '525', '526', '527', '528', '529', '530', '531', '532', '533']

def extract_xml_to_tmp():
    today_date = datetime.now().date()

    session = requests.Session() 
    user_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/xml"
    }
    for code in LOCAL_AUTHORITY_CODE:
        url = f"https://ratings.food.gov.uk/api/open-data-files/FHRS{code}en-GB.xml" 
        r = session.get(url, headers=user_headers, timeout=30)
        try: 
            r.raise_for_status()
            print(f"{code} - xml 파일 다운로드 시작")
            # production path
            with open(f"/opt/airflow/data/fsa-{code}-{today_date}.xml", 'wb') as f:
            # local path
            # with open('./data/fsa.xml', 'wb') as f:
                f.write(r.content)
            print(f"{code} - xml 파일 /data 에 저장 완료")           
        except requests.exceptions.HTTPError as e:
            print("HTTP error occurred:", e) 
            raise 
        except requests.exceptions.RequestException as e:
            print('A request error occurred', e)
            raise 

# 로컬 테스트. DAG에서 실행되므로 주석처리 
# extract_xml_to_tmp()