import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from docker.types import Mount

sys.path.append('/opt/airflow')
from include.t1_extract import extract_xml_to_tmp
from include.t2_load_to_s3 import load_to_s3
from include.t3_load_stg_to_db import load_to_db


BUCKET_NAME = "london-restaurant-hygiene-data-dy"
AWS_CONN_ID = "aws_s3_conn" 

default_args = {
    'owner': 'dayeonlee',
    'depends_on_past': False,
    'start_date': datetime(2026, 8, 20),
    'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'london_restaurant_hygiene_pipeline',
    default_args=default_args,
    description='XML to S3, PostgreSQL',
    schedule_interval='@daily',
    catchup=False,
) as dag: 
        
    task_1 = PythonOperator(
            task_id="extract_task",
            python_callable=extract_xml_to_tmp,
    )
    # task_2 = PythonOperator (
    #         task_id="load_s3_task", 
    #         python_callable=load_to_s3,
    # )
    task_3 = PythonOperator(
            task_id="load_stg_db_task",
            python_callable=load_to_db,
    )


    task_4 = BashOperator(
        task_id='dbt_run_task',
        bash_command="""
        export DW_USER="$DB_USER" && \
        export DW_PASSWORD="$DB_PASSWORD" && \
        export DW_HOST="$DB_HOST" && \
        export DW_PORT="$DB_PORT" && \
        export DW_DB="$DB_NAME" && \
        export XDG_CACHE_HOME="/opt/airflow/.cache" && \
        cd /opt/airflow/dbt_project && dbt run --profiles-dir .
        """
    )

    # dependency 설정 
    # task_1 >> [task_2, task_3]
    task_1 >> [task_3] #임시
    task_3 >> task_4 
