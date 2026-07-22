# 🚀 London FSA Hygiene Data Pipeline Project
> **Project Goal:** Apache Airflow를 깊이 이해하고, S3 백업 및 PostgreSQL 적재를 포함한 End-to-End 데이터 파이프라인의 핵심 개념(멱등성, XComs, Connections 등) 마스터하기.

---

## 🗺️ 프로젝트 체크리스트 (Milestones)

### Milestone 0: 인프라 세팅
- [x] Airflow 2 & PostgreSQL 16: Docker Compose를 활용해 로컬 환경에 Apache Airflow(Web UI 포함)과 PostgreSQL을 안정적으로 띄우기
- [x] AWS S3 테스트용 버킷 생성
- [x] Airflow: 하드코딩을 방지하기 위해 Airflow Web UI `Connections` 메뉴에 AWS 자격증명 및 DB 접속 정보 등록하기 

### Milestone 1: Task 1 (Extract) – API ➔ Local `/tmp`
- [ ] 런던 자치구 중 딱 1개(예: Camden)만 타겟팅하여 `requests` 라이브러리를 활용하여 XML 데이터 다운로드 기능 구현하기
- [ ] 수집된 XML 파일을 Airflow 로컬 임시 디렉토리(`/tmp`)에 안전하게 저장하는 로직 작성하기
- [ ] Airflow `PythonOperator`로 감싸서 DAG를 생성하고, Airflow UI에서 수동(Trigger)으로 실행해 초록 불(Success) 확인하기
- [ ] 태스크 동적 생성으로 33개 보로우 병렬 수집으로 확장하기 

### Milestone 2: Task 2 (Load) – Local `/tmp` ➔ S3
- [ ] 로컬 `/tmp` 디렉토리에 저장된 XML 파일을 읽어 원본 백업을 위해 AWS S3 버킷에 업로드하기

### Milestone 3: Task 3 (Load & Transform) – Local `/tmp` ➔ DB
- [ ] XML 데이터 파싱 및 필요한 핵심 컬럼만 정제(추출)하는 로직 구현하기. Xpath
- [ ] 식당 고유 ID를 기본키(Primary Key)로 활용하여 PostgreSQL 마스터 테이블(Schema) 설계하기
- [ ] 정제된 데이터를 Data Warehouse(DW)에 중복 없이 반영할 수 있도록 `Upsert` 로직 구현하기
- [ ] 업데이트된 PostgreSQL 마스터 테이블에서 아래 3가지 조건의 타겟 데이터를 골라내는 가공(Transform) SQL 쿼리 작성하기
  - [ ] 1) 이번 주 위생등급이 0~2점으로 업데이트된 우려 식당 리스트
  - [ ] 2) 유저 즐겨찾기 테이블과 JOIN하여 0~2점이 뜬 찜한 식당 리스트

### Milestone 4: Task 4 (Cleanup) – Remove Local Files
- [ ] 파이프라인 실행 완료 후 Airflow 로컬 `/tmp` 디렉토리에 남아있는 임시 XML 파일 삭제 로직 구현하기
- [ ] 파이프라인 성공/실패 여부와 관계없이(Trigger Rule 활용 등) 로컬 디스크 공간이 안정적으로 관리되도록 예외 처리 적용하기

### Milestone 5: Task 5 (Alert) – Slack Notification
- [ ] Task 3, 4는 독립적인 태스크로 의존성 설계 
- [ ] 테스트용 슬랙 채널을 개설하고 알림을 받을 수 있는 Incoming Webhook URL 발급받기 또는 Slack Operator 설정하기
- [ ] Task 3에서 만들어진 데이터 바탕으로 운영팀에 보낼 리포트 슬랙으로 전송
~~- [ ] 태스크 성공/실패 여부 알람~~

---
## ⏱️ 데이터 파이프라인 최종 운영 스케줄
* **실행 주기:** 주 1회 (매주 월요일 새벽 05:00 가동)
* **테스트 규칙:** 개발 및 디버깅 중에는 `catchup=False`를 활성화하고, Airflow UI에서 수동 Trigger 버튼을 활용하여 1분 단위로 빠른 피드백 루프 돌리기


====
## 1단계: 슈도코드(의사코드) 먼저 작성하기
코드를 바로 짜기 전에, "한국어"나 간단한 로직 흐름으로 먼저 노트나 메모장에 적어보세요

## 2단계: 모르는 문법과 라이브러리 직접 검색하기
슈도코드를 실제 파이썬 코드로 옮길 때, 막히는 문법이나 함수가 생깁니다.

예: "파이썬에서 requests로 xml 받아올 때 text 속성을 쓰나 content를 쓰나?", "파이썬 파일 쓰기 모드는 뭐였지?"

## 3단계: 나만의 코드로 초안 완성 후, AI에게 코드 리뷰 요청하기
직접 작성한 코드가 완벽하지 않아도 됩니다. 동작하지 않아도 괜찮으니 일단 코드를 작성해 보세요.

그리고 저에게 이렇게 요청해 주세요:

"Task 1 초안을 이렇게 짜봤는데, 에러가 나거나 개선할 부분이 있을까? 내 코드를 고치기 위한 힌트만 줘!"

## 4단계: 트러블슈팅(에러 해결) 즐기기
Airflow나 DB 연동을 하다 보면 수많은 에러(Connection Error, Path Error 등)를 만나게 됩니다.

에러 메시지를 마주했을 때 곧바로 답을 찾기보다, 에러 로그를 읽고 원인을 추론해 보고, 도저히 안 될 때 AI에게 가이드를 요청하세요.