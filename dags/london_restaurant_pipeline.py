from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from include.t1_extract import extract_xml_to_tmp
from include.t2_load_to_s3 import load_to_s3

BUCKET_NAME = "london-restaurant-hygiene-data-dy"
AWS_CONN_ID = "aws_s3_conn" 

default_args = {
    'owner': 'dayeonlee',
    'depends_on_past': False,
    'start_date': datetime(2026, 7, 1),
    'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'london_restaurant_hygiene_pipeline',
    default_args=default_args,
    description='XML to S3, PostgreSQL',
    schedule_interval='@weekly', # 테스트 목적으로 데일리, 매일 밤 00:00(UTC)에 실행
    catchup=False,
) as dag: 
        
    task_1 = PythonOperator(
            task_id="extract_task",
            python_callable=extract_xml_to_tmp,
    )
    task_2 = PythonOperator (
            task_id="load_s3_task", 
            python_callable=load_to_s3,
    )

    # dependency 설정 
    task_1 >> task_2
    
# # TODO: task_2, task_3, task_4, task_5 정의하고 의존성 연결하기
#     # task1 끝나야 2,3 가능 
#     task_1 >> [task_2, task_3]
#     # 2,3 끝나고나서 4 지울수 있음
#     [task_2, task_3] >> task_4
#     # 2,3 끝나면 알람 보낼 수 있음 성공여부, 실패여부/ 3만 끝나도 운영팀 슬랙 보낼 수 있음
#     [task_2, task_3] >> task_5

