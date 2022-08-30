from datetime import datetime, timedelta

from airflow.operators.python_operator import PythonOperator
from airflow import DAG

from av_tasks.collect_files import collect_files
from av_tasks.create_directories import create_directories

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email': ['bonej@ceu.edu', 'danij@ceu.edu', 'krolikowskid@ceu.edu'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# DAG
audio_workflow = DAG(
    dag_id='audio-workflow',
    description='Creates AIPs for audio containers',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
)

# Tasks
collect_audio_files = PythonOperator(
    task_id='collect_audio_files',
    python_callable=collect_files,
    dag=audio_workflow)

create_directories = PythonOperator(
    task_id='create_directories',
    python_callable=create_directories,
    dag=audio_workflow)

# Flow
collect_audio_files >> create_directories
