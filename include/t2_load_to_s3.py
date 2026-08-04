from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime 
from include.constants import LOCAL_AUTHORITY_CODE
from airflow.models import Variable


def load_to_s3():
    print("s3 업로드 시작")
    today_date = datetime.now().date()
    
    failed_list = []     # 실패 결과 추적 (observability)
    AWS_CONN_ID = "aws_s3_conn"
    #S3Hook 인스턴스 생성
    s3_hook = S3Hook(aws_conn_id=AWS_CONN_ID)
    # airflow Variable에서 S3 버킷 이름 가져오기
    BUCKET_NAME = Variable.get("s3_bucket_name")
    
    for code in LOCAL_AUTHORITY_CODE:
        file_name = f"fhrs-{code}-{today_date}.xml"
        try: 
            file_path = f"/opt/airflow/data/{today_date}/{file_name}"
            # S3에 저장될 경로 
            s3_key = f"raw-data/code={code}/date={today_date}/{file_name}"

            s3_hook.load_file(
                filename=file_path,
                key=s3_key,
                replace=True,
                bucket_name=BUCKET_NAME
            )
            print(f"s3 업로드 성공: {file_name}")

        except Exception as e:
            print(f"s3 업로드 실패: {file_name}, 원인: {str(e)}")
            failed_list.append((file_name, str(e)))
    
    if len(failed_list) > 0:
        raise Exception(f"일부 파일 업로드 실패({len(failed_list)}개): {failed_list}")
    else:
        print("33개 xml 파일 성공적으로 S3 업로드")






