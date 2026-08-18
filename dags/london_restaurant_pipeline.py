import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.python import PythonOperator
from docker.types import Mount

from include.t1_extract import extract_xml_to_tmp
from include.t2_load_to_s3 import load_to_s3
from include.t3_load_stg_to_db import load_to_db


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
    schedule_interval='@weekly',
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
    task_3 = PythonOperator(
            task_id="load_stg_db_task",
            python_callable=load_to_db,
    )
    # task_4 = DockerOperator(
    #         task_id="dbt_debug_task",
    #         image="my_dbt_project:latest",
    #         # 나중에 폴더명 변경 필요 
    #         command=[
    #             "debug",
    #             "--profiles-dir",
    #             ".",
    #             "--project-dir",
    #             ".",
    #         ],
    #         docker_url="unix://var/run/docker.sock",
    #         mount_tmp_dir=False,
    #         auto_remove=True,
    #         do_xcom_push=False,
    #         environment={
    #         "DW_DB": os.environ.get("DW_DB", ""),
    #         "DW_USER": os.environ.get("DW_USER", ""),
    #         "DW_PASSWORD": os.environ.get("DW_PASSWORD", ""),
    #         },
    # )
    task_4 = DockerOperator(
    task_id='dbt_run_task',
    image='my_dbt_project:latest',
    auto_remove=True,
    force_pull=False,
    command='run --profiles-dir /usr/app/dbt_project --project-dir /usr/app/dbt_project', 
    docker_url='unix://var/run/docker.sock',
    network_mode='london-restaurant-hygiene-pipeline_default',
    mount_tmp_dir=False,
    environment={
            "DW_DB": os.environ.get("DW_DB", ""),
            "DW_USER": os.environ.get("DW_USER", ""),
            "DW_PASSWORD": os.environ.get("DW_PASSWORD", ""),
            },
)

    # dependency 설정 
    task_1 >> [task_2, task_3]
    # task_1 >> [task_3] #임시
    task_3 >> task_4 
