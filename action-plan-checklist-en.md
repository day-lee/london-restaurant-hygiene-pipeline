# 🚀 London FSA Hygiene Data Pipeline Project
> **Project Goal:** Gain a deep understanding of Apache Airflow and master core data engineering concepts (Idempotence, XComs, Connections, etc.) through building an end-to-end data pipeline featuring S3 backup and PostgreSQL loading.

---

## 🗺️ Project Checklist (Milestones)

### Milestone 0: Infrastructure Setup
- [ ] **Airflow & PostgreSQL**: Spin up Apache Airflow (including the Web UI) and PostgreSQL reliably in a local development environment using Docker Compose.
- [ ] **AWS S3**: Provision a test S3 bucket for data staging.
- [ ] **Airflow Security**: Register AWS credentials and database connection details within the Airflow Web UI `Connections` menu to avoid hardcoding sensitive data.

### Milestone 1: Task 1 (Ingestion) – FSA ➔ S3
- [ ] **API Scripting**: Write a Python script using the `requests` library to fetch XML data, targeting just one single London borough (e.g., Camden) to keep the initial development loop fast.
- [ ] **S3 Streaming**: Implement a streaming upload logic using `boto3` to push the data directly from an in-memory buffer into the S3 bucket without saving files to the local hard drive.
- [ ] **Airflow Integration**: Wrap this ingestion script inside a `PythonOperator` to create a DAG, then manually trigger it from the Airflow UI to verify a successful green run.

### Milestone 2: Task 2 (Load) – S3 ➔ DB
- [ ] **Database Schema**: Design a PostgreSQL master table schema, setting the unique establishment ID as the Primary Key.
- [ ] **XML Parsing**: Write a logic to read the raw XML data back from S3 and parse out only the essential fields.
- [ ] **Data Reliability**: Implement a **UPSERT (Insert or Update) idempotent** SQL logic ensuring that running the same task repeatedly updates existing entries without causing duplication or crashes.

### Milestone 3: Task 3 (Transform & Alert) – DB ➔ Slack
- [ ] **Data Transformation**: Draft SQL queries to extract targeted risk data from the updated PostgreSQL master table based on three specific conditions:
  - [ ] 1) Establishments newly updated with a critical food hygiene rating of 0-2 this week.
  - [ ] 2) At-risk restaurants whose ratings have actively dropped compared to their previous score.
  - [ ] 3) A list of matching high-risk (0-2) restaurants joined with a mock user favourites table.
- [ ] **Slack Integration**: Set up a test Slack channel and generate an Incoming Webhook URL.
- [ ] **Airflow Orchestration**: Use Airflow **XComs (Cross-Communication)** to securely pass the data summary from Task 2 to Task 3 and successfully fire the final markdown report to Slack.

---

## ⏱️ Final Pipeline Production Schedule
* **Execution Frequency:** Once a week (Triggered every Monday at 05:00 AM BST/GMT)
* **Testing Strategy:** Keep `catchup=False` enabled during development and debugging. Use the manual `Trigger DAG` button in the Airflow UI to run instant, minute-by-minute feedback loops.
