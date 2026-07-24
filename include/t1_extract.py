### Milestone 1: Task 1 (Extract) – API ➔ Local `/tmp`
import requests

def extract_xml_to_tmp():
    print("xml 파일 다운로드 시작")

    url = "https://ratings.food.gov.uk/api/open-data-files/FHRS506en-GB.xml" 
    r = requests.get(url)
    with open('/opt/airflow/data/fsa.xml', 'wb') as f:
        f.write(r.content)
    print("xml 파일 /data 에 저장 완료")

# 로컬 테스트. DAG에서 실행되므로 주석처리 
# extract_xml_to_tmp()