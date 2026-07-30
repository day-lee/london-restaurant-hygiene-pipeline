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