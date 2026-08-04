from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from include.t1_extract import extract_xml_to_tmp
from include.t2_load_to_s3 import load_to_s3
from include.t3_load_transform_to_db import load_transform_to_db

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

    task_3 = PythonOperator (
            task_id="load_postgres_task", 
            python_callable=load_transform_to_db,
    )

    # dependency 설정 
    task_1 >> [task_2, task_3]
    

