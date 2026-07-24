### Milestone 1: Task 1 (Extract) – API ➔ Local `/tmp`
import requests

def extract_xml_to_tmp():
    print("xml 파일 다운로드 시작")

    url = "https://ratings.food.gov.uk/api/open-data-files/FHRS506en-GB.xml" 
    r = requests.get(url, timeout=30)
    try: 
        r.raise_for_status()
        # production path
        with open('/opt/airflow/data/fsa.xml', 'wb') as f:
        # local path
        # with open('./data/fsa.xml', 'wb') as f:
            f.write(r.content)
        print("xml 파일 /data 에 저장 완료")           
    except requests.exceptions.HTTPError as e:
        print("HTTP error occurred:", e) 
        raise 
    except requests.exceptions.RequestException as e:
        print('A request error occurred', e)
        raise 

# 로컬 테스트. DAG에서 실행되므로 주석처리 
# extract_xml_to_tmp()