from datetime import timedelta, datetime

from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators.python_operator import PythonOperator

from airflow import DAG

from python_tasks.collect_files import collect_files
from python_tasks.create_directories import create_directories
from python_tasks.copy_master_files import copy_master_files
from python_tasks.create_checksums import create_checksums

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


def retrigger(context, dag_run_obj):
    return dag_run_obj


dag_id = 'osa-av-workflow'
dag = DAG(dag_id=dag_id,
          description='Main DAG for the preservation workflow',
          default_args=default_args,
          schedule_interval=None,
          catchup=False)

task_01 = PythonOperator(task_id='collect_files', python_callable=collect_files, dag=dag)
task_02 = PythonOperator(task_id='create_directories', python_callable=create_directories, dag=dag)
task_03 = PythonOperator(task_id='copy_master_files', python_callable=copy_master_files, dag=dag)
task_04 = PythonOperator(task_id='create_checksums', python_callable=create_checksums, dag=dag)
task_05 = TriggerDagRunOperator(task_id='restart_dag', trigger_dag_id=dag_id, python_callable=retrigger, dag=dag)

task_01.set_downstream(task_02)
task_02.set_downstream(task_03)
task_03.set_downstream(task_04)
task_04.set_downstream(task_05)
