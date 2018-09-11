from datetime import timedelta, datetime
from pathlib import Path

from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator

from airflow import DAG

from python_tasks.collect_files import collect_files
from python_tasks.create_directories import create_directories
from python_tasks.copy_master_files import copy_master_files
from python_tasks.create_checksums import create_checksums
from python_tasks.encode_masters import encode_masters
from python_tasks.create_video_info import create_video_info
from python_tasks.send_email import notify_email

from python_tasks.config import INPUT_DIR, MASTER_FILE_EXTENSION, ACCESS_FILE_EXTENSION


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


def retrigger_dag(context, dag_run_obj):
    pathlist = list(Path(INPUT_DIR).glob('**/*.%s' % MASTER_FILE_EXTENSION))
    if len(pathlist) > 0:
        return dag_run_obj
    else:
        return None


# DAG
dag = DAG(dag_id='osa-av-workflow',
          description='Main DAG for the preservation workflow',
          default_args=default_args,
          schedule_interval=None,
          catchup=False)

# Tasks
collect_files = PythonOperator(
    task_id='collect_files',
    python_callable=collect_files,
    dag=dag)

create_directories = PythonOperator(
    task_id='create_directories',
    python_callable=create_directories,
    dag=dag)

copy_master_files = PythonOperator(
    task_id='copy_master_files',
    python_callable=copy_master_files,
    dag=dag)

create_master_checksums = PythonOperator(
    task_id='create_master_checksums',
    python_callable=create_checksums,
    dag=dag,
    op_kwargs={
        'directory': 'Preservation',
        'file_extension': MASTER_FILE_EXTENSION
    })

create_master_info = PythonOperator(
    task_id='create_master_info',
    python_callable=create_video_info,
    dag=dag,
    op_kwargs={
        'directory': 'Preservation',
        'file_extension': MASTER_FILE_EXTENSION
    })

encode_masters = BranchPythonOperator(
    task_id='encode_masters',
    python_callable=encode_masters,
    dag=dag,
    op_kwargs={
        'on_success': 'create_access_checksums',
        'on_error': 'break_dag'
    })

create_access_checksums = PythonOperator(
    task_id='create_access_checksums',
    python_callable=create_checksums,
    dag=dag,
    op_kwargs={
        'directory': 'Access',
        'file_extension': ACCESS_FILE_EXTENSION
    })

create_access_info = PythonOperator(
    task_id='create_access_info',
    python_callable=create_video_info,
    dag=dag,
    op_kwargs={
        'directory': 'Access',
        'file_extension': ACCESS_FILE_EXTENSION
    })

break_dag = DummyOperator(
    task_id='break_dag',
    dag=dag)

retrigger_dag = TriggerDagRunOperator(
    task_id='restart_dag',
    trigger_dag_id=dag_id,
    python_callable=retrigger_dag,
    dag=dag,
    trigger_rule='one_success')

send_info_mail = PythonOperator(
    task_id='send_info_mail',
    python_callable=notify_email,
    dag=dag)

# Flow
collect_files.set_downstream(create_directories)
create_directories.set_downstream(copy_master_files)
copy_master_files.set_downstream(create_master_checksums)
create_master_checksums.set_downstream(create_master_info)
create_master_info.set_downstream(encode_masters)
encode_masters.set_downstream(create_access_checksums)
create_access_checksums.set_downstream(create_access_info)
create_access_info.set_downstream(send_info_mail)
send_info_mail.set_downstream(retrigger_dag)

# Error branch
encode_masters.set_downstream(break_dag)
break_dag.set_downstream(send_info_mail)
send_info_mail.set_downstream(retrigger_dag)


