import os
from datetime import timedelta, datetime
from pathlib import Path

from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator

from airflow import DAG

from av_tasks.collect_files import collect_files
from av_tasks.create_directories import create_directories
from av_tasks.copy_master_files import copy_master_files
from av_tasks.create_checksums import create_checksums
from av_tasks.encode_masters import encode_masters
from av_tasks.create_low_quality_access import create_low_quality
from av_tasks.create_video_info import create_video_info
from av_tasks.send_email import notify_email
from av_tasks.get_descriptive_metadata import get_descriptive_metadata
from av_tasks.push_to_ams import push_to_ams


INPUT_DIR = os.environ.get("AV_INPUT_DIR", default='/opt/input')
MASTER_FILE_EXTENSION = os.environ.get("AV_MASTER_FILE_EXTENSION")
ACCESS_FILE_EXTENSION = os.environ.get("AV_ACCESS_FILE_EXTENSION")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 1, 1),
    'email': ['bonej@ceu.edu', 'danij@ceu.edu', 'krolikowskid@ceu.edu'],
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


# DAGS
osa_av_workflow = DAG(
    dag_id='osa-av-workflow',
    description='Main DAG for the AV preservation workflow',
    default_args=default_args,
    schedule_interval=None,
    catchup=False)


# Tasks
collect_files = PythonOperator(
    task_id='collect_files',
    python_callable=collect_files,
    dag=osa_av_workflow)

create_directories = PythonOperator(
    task_id='create_directories',
    python_callable=create_directories,
    dag=osa_av_workflow)

copy_master_files = PythonOperator(
    task_id='copy_master_files',
    python_callable=copy_master_files,
    dag=osa_av_workflow)

create_master_checksums = PythonOperator(
    task_id='create_master_checksums',
    python_callable=create_checksums,
    dag=osa_av_workflow,
    op_kwargs={
        'directory': 'Preservation',
        'file_extension': MASTER_FILE_EXTENSION
    })

create_master_info = PythonOperator(
    task_id='create_master_info',
    python_callable=create_video_info,
    dag=osa_av_workflow,
    op_kwargs={
        'directory': 'Preservation',
        'file_extension': MASTER_FILE_EXTENSION
    })

get_descriptive_metadata = PythonOperator(
    task_id='get_descriptive_metadata',
    python_callable=get_descriptive_metadata,
    dag=osa_av_workflow
    )

push_to_ams = PythonOperator(
    task_id='push_to_ams',
    python_callable=push_to_ams,
    dag=osa_av_workflow
    )
    
encode_masters = BranchPythonOperator(
    task_id='encode_masters',
    python_callable=encode_masters,
    dag=osa_av_workflow,
    op_kwargs={
        'on_success': 'create_access_checksums',
        'on_error': 'break_dag'
    })

create_low_quality_access_copy = PythonOperator(
    task_id='create_low_access',
    python_callable=create_low_quality,
    dag=osa_av_workflow
    )

break_dag = DummyOperator(
    task_id='break_dag',
    dag=osa_av_workflow)

send_info_mail = PythonOperator(
    task_id='send_info_mail',
    python_callable=notify_email,
    dag=osa_av_workflow,
    trigger_rule='one_success')

retrigger_dag = TriggerDagRunOperator(
    task_id='restart_dag',
    trigger_dag_id='osa-av-workflow',
    python_callable=retrigger_dag,
    dag=osa_av_workflow)

# Flow
collect_files.set_downstream(create_directories)
create_directories.set_downstream(copy_master_files)
copy_master_files.set_downstream(create_master_checksums)
create_master_checksums.set_downstream(create_master_info)
create_master_info.set_downstream(get_descriptive_metadata)
get_descriptive_metadata.set_downstream(push_to_ams)
push_to_ams.set_downstream(encode_masters)
encode_masters.set_downstream(create_low_quality_access_copy)
create_low_quality_access_copy.set_downstream(send_info_mail)
send_info_mail.set_downstream(retrigger_dag)

# Error branch
encode_masters.set_downstream(break_dag)
break_dag.set_downstream(send_info_mail)
