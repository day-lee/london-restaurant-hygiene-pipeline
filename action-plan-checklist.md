# 🚀 London FSA Hygiene Data Pipeline Project
> **Project Goal:** Apache Airflow를 깊이 이해하고, S3 백업 및 PostgreSQL 적재를 포함한 End-to-End 데이터 파이프라인의 핵심 개념(멱등성, XComs, Connections 등) 마스터하기.

---

## 🗺️ 프로젝트 체크리스트 (Milestones)

### Milestone 0: 인프라 세팅
- [x] Airflow 2 & PostgreSQL 16: Docker Compose를 활용해 로컬 환경에 Apache Airflow(Web UI 포함)과 PostgreSQL을 안정적으로 띄우기
- [x] AWS S3 테스트용 버킷 생성
- [x] Airflow: 하드코딩을 방지하기 위해 Airflow Web UI `Connections` 메뉴에 AWS 자격증명 및 DB 접속 정보 등록하기 

### Milestone 1: Task 1 (Ingestion) – FSA ➔ S3
- [x] 런던 자치구 중 딱 1개(예: Camden)만 타겟팅하여 `requests` 라이브러리로 XML 데이터 가져오는 파이썬 스크립트 작성하기
- [x] 로컬 디스크 저장 없이 메모리 버퍼에서 `boto3`를 사용하여 S3 버킷으로 바로 쏴주는 스트리밍 업로드 로직 구현하기
- [x] Airflow: 이 수집 스크립트를 `PythonOperator`로 감싸서 DAG를 생성하고, Airflow UI에서 수동(Trigger)으로 실행해 초록 불(Success) 확인하기
- [] 태스크 동적 생성으로 33개 보로우 병렬 수집으로 확장하기 

### Milestone 2: Task 2 (Load) – S3 ➔ DB
- [ ] 식당 고유 ID를 기본키(Primary Key)로 설정하여 PostgreSQL 마스터 테이블(Schema) 설계하기
- [ ] S3에 저장된 XML 데이터를 파이썬으로 다시 읽어와 필요한 핵심 필드만 골라내는 파싱 로직 작성하기
- [ ] 같은 태스크를 여러 번 연속으로 돌려도 데이터가 중복 적재되지 않고 최신화되는 **UPSERT(Insert or Update) 멱등성** SQL 로직 구현하기

### Milestone 3: Task 3 (Transform & Alert) – DB ➔ Slack
- [ ] 업데이트된 PostgreSQL 마스터 테이블에서 아래 3가지 조건의 타겟 데이터를 골라내는 가공(Transform) SQL 쿼리 작성하기
  - [ ] 1) 이번 주 위생등급이 0~2점으로 업데이트된 우려 식당 리스트
  - [ ] 2) 이전 등급보다 점수가 하락한 리스크 식당 리스트
  - [ ] 3) 유저 즐겨찾기 테이블과 JOIN하여 0~2점이 뜬 찜한 식당 리스트
- [ ] 테스트용 슬랙 채널을 개설하고 알림을 받을 수 있는 Incoming Webhook URL 발급받기
- [ ] Airflow: Task 2에서 처리된 데이터 요약본을 **XComs(태스크 간 통신)**를 통해 Task 3으로 안전하게 넘겨받아 슬랙 알림 메시지 최종 발송 성공하기

---

## ⏱️ 데이터 파이프라인 최종 운영 스케줄
* **실행 주기:** 주 1회 (매주 월요일 새벽 05:00 가동)
* **테스트 규칙:** 개발 및 디버깅 중에는 `catchup=False`를 활성화하고, Airflow UI에서 수동 Trigger 버튼을 활용하여 1분 단위로 빠른 피드백 루프 돌리기
