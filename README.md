<<<<<<< Updated upstream
## 💡 Project Overview

* **System:** Hybrid (Local & Cloud) ELT pipeline built with **Apache Airflow**.
* **Data:** London restaurant food hygiene ratings [(**FSA Open Data**)](https://ratings.food.gov.uk/open-data).
* **Data Volume:** Processes **~81k active restaurant records** per weekly batch run.
* **Data Modeling Strategy:** Implemented **SCD (Slowly Changing Dimension) Type 2** logic to track rating evolution over time
* **Impact:** Weekly insights for a (hypothetical) delivery ops team to mitigate operational risks.

<p align="center">
  <img width="400" alt="image" src="https://github.com/user-attachments/assets/3ee19476-a727-4c63-8cd3-f330431fd4ff" />
  <img width="200" alt="delivery" src="https://github.com/user-attachments/assets/5b8893da-6518-4743-90d2-aaea0ac896d0" />
</p>

## 🔍 Architecture Diagram 

<p align="center">
  <img width="800" alt="diagram" src="https://github.com/user-attachments/assets/76c57a74-e6f0-4023-8db1-71597974033c" />
</p>

### Architecture Components

* **Environment Strategy**: The Local Path serves as a sandbox for rapid, repeatable testing, while the Cloud Path drives the automated production environment.
* **Local Path:** AWS S3 (Raw Data Lake) -> PostgreSQL (Data Warehouse) -> dbt (Transformation)
* **Cloud Path:** Fly.io (Runtime) -> GitHub Actions (Scheduler) -> Supabase Postgres (Data Warehouse) -> dbt (Transformation)
* **Orchestration:** Apache Airflow (Docker-based environment)
* **WIP:** GCP BigQuery Migration

## 📊 [Dashboard & Insights](https://datastudio.google.com/s/v_uXnzzJjig) 

<p align="center">
  <a href="https://datastudio.google.com/s/v_uXnzzJjig" target="_blank">
    <img width="600" alt="dashboard" src="https://github.com/user-attachments/assets/02a97a13-3b66-4884-ae83-543fb0c5b063" />
  </a>
</p>

## 🛠️ Data Pipeline Details

### Ingestion
* **Strategy:** Opted for batch XML downloads over API ingestion.
* **Rationale:** Maximises stability since the source data does not require real-time updates.

### Data Warehousing & Modeling (dbt)
* **Staging:** Flattened and parsed raw XML data into staging tables.
* **Core Layer:** Modelled data into decoupled Dimension and Fact tables.
* **Mart Layer:** Materialised analytics-ready tables tailored for reporting.

### Why Dual Paths? (Architecture Isolation)
* **Local Path (S3 + Postgres):** Dedicated to safe local development and debugging.
* **Cloud Path (Fly.io + Supabase):** A lightweight, serverless production environment.
* **FinOps & Stability:** Minimises cloud spend by keeping dev/test environments local, while improving production stability through strict architecture isolation.

Airflow web dashboard: https://london-restaurant-hygiene-pipeline.fly.dev/
