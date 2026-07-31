# Data Engineering Core Concepts 

## 1. OLTP vs OLAP (Operational vs. Analytical Databases)

Understanding the fundamental split between transactional processing and modern analytical data warehousing is critical.

### OLTP (Online Transaction Processing)
* **Purpose**: Designed to handle real-time, high-concurrency insertions and updates line-by-line (e.g., banking apps, e-commerce checkouts).
* **Architecture**: Highly **Normalized** (3NF) to minimize data redundancy and guarantee ACID transactions.
* **Technology**: PostgreSQL, MySQL.

### OLAP (Online Analytical Processing)
* **Purpose**: Designed for high-performance analytical queries that aggregate millions of rows at once (e.g., calculating the average hygiene score per borough).
* **Architecture**: Highly **Denormalized** (Star Schema / Snowflake Schema) to eliminate complex queries and maximize read performance.
* **Technology**: Snowflake, Google BigQuery, AWS Redshift.

---

## 2. Idempotency (멱등성)

The golden rule of building production-grade data pipelines.

* **Definition**: An idempotent pipeline guarantees that **running it once produces the exact same final state as running it multiple times** consecutively with the same input.
* **Project Context**: In our pipeline, implementing a **Truncate & Load** approach for the Staging Layer (`stg_fhrs__establishments`) enforces strict idempotency. If a weekly cron job accidentally triggers three times, it safely overwrites the temporary staging table rather than appending duplicated rows.

---

## 3. Incremental Load (증분 적재)

Optimizing pipeline cost and execution runtime in the cloud.

* **Definition**: Instead of reading the entire historical dataset (e.g., 10 years of restaurant records) during every execution cycle, an incremental pipeline selectively extracts only **newly created or updated records** since the last execution timestamp.
* **Benefit**: Dramatically reduces cloud compute costs (AWS/GCP), API network bandwidth, and warehouse processing times.

---

## 4. dbt (Data Build Tool)

The standard modern data stack (MDS) orchestration framework across London data teams.

* **Definition**: An open-source workflow tool that enables data engineers to write modular, version-controlled transformations inside the data warehouse using plain **SQL and Jinja**.
* **Why it matters**: It automatically orchestrates the lineage from your Staging Layer to your Fact and Dimension tables, embeds automated data quality testing (`not_null`, `unique`), and auto-generates documentation/ERDs out of the box. Mentioning dbt proficiency instantly shifts your profile from an aspiring junior to a production-ready engineer.

---

## 5. DL vs DW vs DM
* ** 데이터 레이크 DL
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
- 데이터 웨어하우스 DW 전문 솔루션: 대용량 분석에 특화된 AWS Redshift, Google BigQuery, SnowFlake 
- structured tables
- BI, SQL Analytics

#### 데이터 마트 DM
- structured
- "특정 부서" 대상 (내 플젝은 운영팀)
- 작고 단순하게 구성되어 빠른 쿼리 속도로 현업 담당자들이 바로 쓸수 있게 가공되어 있음 
- 100 GB 이하
