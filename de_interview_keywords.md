# Data Engineering Core Concepts 

## 0. ETL/ ELT
* **extract**: 원유(데이터)를 땅에서 파옴
* **loading**: 공장 저장탱크에 한데 모음(Datalake)
* **transformation**: 원유를 가공해 휘발유, 등유 등으로 제품화. 
- 트렌스폼의 결과물: stg(일단 덤프한 데이터) -> fact, dim table, mart table로 분리(사용자가 바로 쓸 수 있는 제품 형태로 만듦)
- DE에서 트랜스폼의 의미: 소스 데이터(json, xml, sql)에서 `RDB 구조(겉모습)로 변경`되고, `비즈니스 의미`를 가지게된다(내부) 

* ELT (modern)
- with cloud service, we can store as many raw data, near real time processing 
- data governance issue 

* ETL (traditional)
- saving the memory as transformation is already done
- Good for data governance (store only necessary information)
- it can be slow as transformation takes more time 


## 1. OLTP vs OLAP (Operational vs. Analytical Databases)

transactional processing vs modern analytical data warehousing

### OLAP (Online Analytical Processing)
* **Purpose**: Designed for high-performance analytical queries that aggregate millions of rows at once. For business decision.
* **Architecture**: Highly **Denormalized** (Star Schema / Snowflake Schema) to eliminate complex queries and maximize read performance.
* **Technology**: Snowflake, Google BigQuery, AWS Redshift.
* OLAP Data Cube: Multidimensional data representation: data slicing

### OLTP (Online Transaction Processing)
* **Purpose**: Designed to handle real-time, high-concurrency insertions and updates. 
 - (e.g., banking apps, e-commerce checkouts).
* **Architecture**: Highly **Normalized** (3NF) to minimize data redundancy and guarantee ACID transactions.
* **Technology**: PostgreSQL, MySQL.


---

## 2. Idempotency (멱등성)

The golden rule of building production-grade data pipelines.

* **Definition**: An idempotent pipeline guarantees that **running it multiple times produces the exact same final state as running it once** with the same input.
* **Project Context**:  **Truncate & Load** approach for the Staging Layer (`stg_fhrs__establishments`) enforces strict idempotency. If a weekly cron job accidentally triggers three times, it safely overwrites the temporary staging table rather than appending duplicated rows.

---

## 3. Incremental Load (증분 적재)

Optimizing pipeline cost and execution runtime in the cloud.

* **Definition**: Instead of reading the entire historical dataset (e.g., 10 years of restaurant records) during every execution cycle, an incremental pipeline selectively extracts only **newly created or updated records** since the last execution timestamp.
* **Benefit**: Dramatically reduces cloud compute costs (AWS/GCP), API network bandwidth, and warehouse processing times.

---

## 4. dbt (Data Build Tool)

The standard modern data stack (MDS) orchestration framework across London data teams.

* **Definition**: A workflow tool that enables data engineers to write modular, version-controlled transformations inside the data warehouse using plain **SQL and Jinja**.
* **Why it matters**: It automatically orchestrates the lineage from your Staging Layer to your Fact and Dimension tables, embeds automated data quality testing (`not_null`, `unique`), and auto-generates documentation/ERDs out of the box.

---

## 5. DL vs DW vs DM
#### 데이터 레이크 DL
- 로우 데이터 백업: 외부 소스 데이터는 변경되거나 제공 중단 될 수 있음 
- 데이터 가공 목적이 아직 정해지지 않았을 수 있음
- 전체 회사 범위
- 감사 오딧용(data lineage)
- 외부 데이터 접근 불가능: 네트워크 문제 등, pipeline re-run
- data replication, database redundancy 미래 유실 대비 등.. 
- unstructured 데이터: 비디오, 텍스트, 다양한 포맷
- s3는 Single Source of Truth로 사용됨. 
    - s3 glacier는 아카이브 등급으로 과거 데이터 저장가능. 비용이 굉장히 적음 

#### 데이터 웨어하우스 DW
- 회사 전체 데이터 대상 
- 중간에서 upstream, downstream effect가 있어서 복잡한 변화는 어려움
(upstream(영향 받는): 소스데이터의 노드명 변경, downstream(영향 주는): dw에서 변경한 컬럼명이 대시보드가 깨진다. )
- 비즈니스에 필요한 핵심 필드만 가공해서 postgreSQL에 upsert함 
- 데이터 웨어하우스 DW 전문 솔루션: Big Data - AWS Redshift, Google BigQuery, SnowFlake 
- structured tables
- BI, SQL Analytics

#### 데이터 마트 DM
- structured
- Specific user: "특정 부서" 대상 (내 플젝은 운영팀)
- 작고 단순하게 구성되어 빠른 쿼리 속도로 현업 담당자들이 바로 쓸수 있게 가공되어 있음 
- 100 GB 이하


## 6. Data as a Product 
- Data Analysts, Data Scientist가 제품(DW, DM)의 내부 고객임.  
- 제품은 신뢰성(데이터 정합성), 사용성(일관된 가이드, 메타데이터), 신속성(쿼리 성능 최적화)을 보장해야함 

- 사용자 중심 설계: DA/DS가 쿼리를 짤 때 자주 조인이 필요한 테이블은 미리 마트로 만들거나 사용하기 쉽게 다듬어둠
- 데이터 계약: 소스 시스템 변경으로 DA/DS 분석 대시보드가 망가지지 않도록 구조 관리
- 지속 피드백: DA/DS가 데이터 활용 중 겪는 불편함(페인 포인트)를 알고 개선함


## 7. Star, Snowflake Schema - Kimball approach
- 순서가 Top-down과 반대임. Data Mart -> Data Warehouse 
### Fact table: 
- single central table, metrics, measurement, fact about org 
### Dimension table:
- multiple dim tables, reference table. details, characters, attributes e.g. customer name, email, country...

#### Start Schema, Snowflake Schema 
- richer dataset: dim table connected through another dim table

## 8. Kimball 4 step process
1. **Select orginisation process**: invoice, marketing -> start with one department 
2. **Declare the grain**: level to store fact table. 더이상 쪼갤 수 없는 Music service -> Song grain 
3. **Identify the dimensions**: time(year, month). location(address, country). users(name, email)
4. **Identify the fact**: e.g. music service: total number of plays, sales revenue of a song 
-> what are we answering? 

### SCD - Slowly Changing Dimensions


### Data Cleaning 
1. Data format cleaning: date, capitalization, address parsing
2. Data validation: type check, range check(age can't be 300) 
3. Deduplication: gets rid of duplicate entries 
4. Data governance: is a set of organizational policies and processes to help keep the data clean


## 9. Tabular source, Columnar 

### Tabular Source(정형 structured 데이터 소스) 
- 행과 열을 가진 테이블 형식 
- Parguet: 데이터 엔지니어링에서 가장 많이 쓰는 열 기반(Columnar) 정형 파일 형식입니다.
- Row based 행 기반 - 트랜잭션용: MySQL, PostgreSQL, Oracle
- Column based 열 기반 - 분석/DW용: Google BigQuery, Snowflake, AWS Redshift

### Columnar data 열기반 
#### Pandas
- 판다스는 시리즈(열 기반)가 연속되어서 묶여있다. 
- 벡터화(Vectorization): C언어로 구현된 내부 엔진(NumPy 기반)이 메모리에 일렬로 나열된 열(Column) 데이터를 통째로 가져와 한 번에 연산한다. 
#### BigQuery
- 각 열이 별도로 저장되고 각 열에 대한 인덱스를 포함한다 
- capacitor에 저장
- colossus 분산 처리