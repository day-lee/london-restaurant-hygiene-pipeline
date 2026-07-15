from datetime import datetime, timedelta
import requests
from io import BytesIO 

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook 

BUCKET_NAME = "london-restaurant-hygiene-data-dy"
AWS_CONN_ID = "aws_s3_conn" 

default_args = {
    'owner': 'dayeonlee',
    'depends_on_past': False,
    'start_date': datetime(2026, 7, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'london_restaurant_hygiene_pipeline',
    default_args=default_args,
    description='step1: XML to S3',
    schedule_interval='@daily', # 테스트 목적으로 데일리
    catchup=False,
) as dag: 

    def _extract_xml_to_s3_streaming(**kwargs):
        # restaurant in camden hygiene rating download 
        url = "https://ratings.food.gov.uk/api/open-data-files/FHRS506en-GB.xml" 
        print(f"FSA XML file download starts: {url}")
        #stream=True option으로 데이터를 메모리에 올리지 않고 스트림으로 읽어옴 
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            # 로컬 디스크 I/O없이 메모리 상에 바이너리 버퍼 bytesIO 생성   
            memory_buffer = BytesIO() 
            # 대용량 파일일 경우 대비해 청크 단위로 쪼개서 메모리 버퍼에 기록 
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    memory_buffer.write(chunk)
            # 버퍼 포인터를 맨 앞으로 돌려 읽을 준비 
            memory_buffer.seek(0)
            print("메모리 버퍼에 xml 데이터 로드 완료. 로컬 디스트 저장 X")
            # Airflow 내장 S3Hook(내부 boto3 사용) 해서 S3 스트리밍 업로드 
            s3_hook = S3Hook(aws_conn_id=AWS_CONN_ID)

            logical_date = kwargs['ds_nodash']
            s3_key = f"raw/camden_restaurant_hygiene_{logical_date}.xml"

            # load_file_obj 사용하여 파일 객체(버퍼) 채로 s3에 스트리밍 전송 
            s3_hook.load_file_obj(
                file_obj=memory_buffer,
                key=s3_key ,
                bucket_name=BUCKET_NAME,
                replace=True 
            )
            print(f"Successfully uploaded to AWS S3 bucket: s3://{BUCKET_NAME}/{s3_key}")

            # 사용 끝난 메모리 버퍼 닫아 메모리 해제 
            memory_buffer.close() 
        else: 
            raise Exception(f"FSA XML 다운로드 실패: {response.status_code}")
    
    # PythonOperator로 래핑 
    extract_xml_to_s3 = PythonOperator(
        task_id='extract_xml_to_s3_streaming',
        python_callable=_extract_xml_to_s3_streaming,
        provide_context=True 
    )

    extract_xml_to_s3
