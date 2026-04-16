from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.smtp.operators.smtp import EmailOperator
from airflow.providers.papermill.operators.papermill import PapermillOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "victor",
    "depends_on_past": False,
    "email": ["alert@email.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="sports-pipeline",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["sports", "football", "etl"]
) as dag:

    ingest = PapermillOperator(
        task_id="ingest",
        input_nb="notebooks/01_ingest_matches_bronze.ipynb",
        output_nb="/tmp/out_bronze.ipynb",
        dag=dag
    )

    transform = PapermillOperator(
        task_id="transform",
        input_nb="notebooks/02_transform_matches_silver.ipynb",
        output_nb="/tmp/out_silver.ipynb",
        dag=dag
    )

    load = PapermillOperator(
        task_id="load",
        input_nb="notebooks/03_aggregate_matches_gold.ipynb",
        output_nb="/tmp/out_gold.ipynb",
        dag=dag
    )

    email_subject = "Sports Pipeline Report - {{ ds }}"
    email_body = """
    <h3>Sports Pipeline Completed ✅</h3>
    <p>DAG: {{ dag.dag_id }}</p>
    <p>Execution date: {{ ds }}</p>
    <p>Next run: {{ next_ds }}</p>
    """

    email_report = EmailOperator(
        task_id="email_report",
        to="test_mail@email.com",
        subject=email_subject,
        html_content=email_body,
        dag=dag
    )

    ingest >> transform >> load >> email_report