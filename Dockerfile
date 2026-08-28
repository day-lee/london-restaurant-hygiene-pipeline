FROM apache/airflow:2.10.2 

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* 

USER airflow 

RUN pip install --no-cache-dir \
    "protobuf<5" \
    "dbt-core==1.8.2" \
    "dbt-postgres==1.8.7" \
    "psycopg[binary]"

COPY --chown=airflow:root ./dags /opt/airflow/dags
COPY --chown=airflow:root ./dbt_project /opt/airflow/dbt_project
COPY --chown=airflow:root ./include /opt/airflow/include

USER root
RUN mkdir -p /opt/airflow/data && chown -R airflow:root /opt/airflow/data
USER airflow

ENTRYPOINT []

# 컨테이너가 켜질 때 DB 마이그레이션을 하고, 스케줄러를 백그라운드로 띄운 뒤, 웹서버를 메인 프로세스로 상주시켜 컨테이너가 꺼지지 않게 합니다.
CMD ["sh", "-c", "airflow db migrate && (airflow scheduler & exec airflow webserver --hostname 0.0.0.0 --port 8080 --workers 1)"]
