FROM apache/airflow:2.10.2 

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* 

USER airflow 

RUN pip install --no-cache-dir "protobuf<5" "dbt-postgres>=1.8.0,<1.9.0"

COPY --chown=airflow:root ./dbt_project /opt/airflow/dbt_project
