from airflow import DAG
from airlfow.operators.python import PythonOperator 
from datetime import datetime
import time 

with DAG(
    dag_id='dependency_test',
    start_date=datetime(2026, 7, 1),
    schedule=None,
    catchup=False,
) as dag:

    t1_extract = PythonOperator(
        task_id="extract_task",
        python_callable=lambda: (print("Extract 시작"), time.sleep(5), print("Extract 완료")),
    )

    t2_load_s3 = PythonOperator(
        task_id="load_s3_task",
        python_callable=lambda: (print("s3 업로드 시작"), time.sleep(7), print("s3 업로드 완료")),
    )

    t3_load_db = PythonOperator(
        task_id="load_to_db",
        python_callable=lambda: (print("DB 업로드 시작"), time.sleep(7), print("DB 업로드 완료")),
    )

    t4_cleanup_tmp = PythonOperator(
        task_id="cleanup_tmp",
        python_callable=lambda: (print("cleanup 시작"), time.sleep(4), print("cleanup 완료")),
    )

    t5_alert_slack= PythonOperator(
        task_id="slack_alert",
        python_callable=lambda: (print("slack alert 시작"), time.sleep(3), print("slack alert 완료"))
    )

    t1_extract >> [t2_load_s3, t3_load_db]
    [t2_load_s3, t3_load_db] >> t4_cleanup_tmp 
    [t2_load_s3, t3_load_db] >> t5_alert_slack