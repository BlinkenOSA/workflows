from datetime import timedelta

from airflow import DAG

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['bonej@ceu.edu', 'danij@ceu.edu'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('osa-av-workflow', default_args=default_args, schedule_interval=timedelta(1))
