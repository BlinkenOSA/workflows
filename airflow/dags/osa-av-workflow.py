from datetime import timedelta, datetime
from airflow.operators.python_operator import PythonOperator

from airflow import DAG

from python_tasks.collect_files import collect_files, create_directories, copy_master_files

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 1, 1),
    'email': ['bonej@ceu.edu', 'danij@ceu.edu'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('osa-av-workflow',
          description='Main DAG for the preservation workflow',
          default_args=default_args,
          schedule_interval=None,
          catchup=False)

task_01 = PythonOperator(task_id='collect_files', python_callable=collect_files, dag=dag)

task_02 = PythonOperator(task_id='create_directories', python_callable=create_directories, dag=dag)
task_02.set_upstream(task_01)

task_03 = PythonOperator(task_id='copy_master_files', python_callable=copy_master_files, dag=dag)
task_03.set_upstream(task_02)
