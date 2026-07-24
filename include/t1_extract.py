### Milestone 1: Task 1 (Extract) – API ➔ Local `/tmp`
from datetime import datetime 
import requests
import os

LOCAL_AUTHORITY_CODE = ['501', '502', '503', '504', '505', '506', '507', '508', '509', '510', '511', '512', '513', '514', '515', '516', '517', '518', '519', '520', '521', '522', '523', '524', '525', '526', '527', '528', '529', '530', '531', '532', '533']

def extract_xml_to_tmp():
    today_date = datetime.now().date()
    failed_list = []
    session = requests.Session() 
    user_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/xml"
    }
    for code in LOCAL_AUTHORITY_CODE:
        url = f"https://ratings.food.gov.uk/api/open-data-files/FHRS{code}en-GB.xml" 
        production_path_name = f"/opt/airflow/data/fsa-{code}-{today_date}.xml"
        local_path_name = f"./data/fsa-{code}-{today_date}.xml"

        # retry시 이미 존재하는 파일은 건너뜀
        if os.path.exists(production_path_name):
            continue
        try: 
            print(f"{code} - xml 파일 다운로드 시작")
            r = session.get(url, headers=user_headers, timeout=30)
            r.raise_for_status()
            with open(production_path_name, 'wb') as f:
                f.write(r.content)
            print(f"{code} - xml 파일 /data 에 저장 완료")           
        except requests.exceptions.HTTPError as e:
            print("HTTP error occurred:", e) 
            failed_list.append(code)
            continue
        except requests.exceptions.RequestException as e:
            print('A request error occurred', e)
            failed_list.append(code)
            continue
    if len(failed_list) != 0:
        # airflow retry 트리거 위해 
        raise ValueError(f"Failed to download {failed_list}")

# 로컬 테스트. DAG에서 실행되므로 주석처리 
# extract_xml_to_tmp()