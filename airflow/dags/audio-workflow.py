from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from av_tasks.audio.check_barcode_existence import check_barcode
from av_tasks.audio.collect_audio_files import collect_audio_files
from av_tasks.audio.create_dirs import create_dirs

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
# TODO: Tasks should depend on each other
# especially the barcode checker; if it fails, stop the flow
collect_audio_files = PythonOperator(
    task_id='collect_audio_files',
    python_callable=collect_audio_files,
    dag=audio_workflow
)

check_barcode_existence = PythonOperator(
    task_id='check_barcode_existence',
    python_callable=check_barcode,
    dag=audio_workflow
)

create_dirs = PythonOperator(
    task_id='create_directories_for_audio_preservation',
    python_callable=create_dirs,
    dag=audio_workflow
)

# Flow
collect_audio_files.set_downstream(check_barcode_existence)
check_barcode_existence.set_downstream(create_dirs)
