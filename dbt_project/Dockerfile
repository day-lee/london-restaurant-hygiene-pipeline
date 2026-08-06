FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /usr/app/dbt_project

#git 설치
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 필수 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# dbt 프로젝트 소스 코드 복사
COPY . .

# 기본 실행 명령어 (컨테이너가 켜지면 dbt가 바로 실행되도록 함)
ENTRYPOINT ["dbt"]
