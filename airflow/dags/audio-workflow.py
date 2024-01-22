import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator

from av_tasks.audio.check_barcode_existence import check_barcode
from av_tasks.audio.collect_audio_files import collect_audio_files
from av_tasks.audio.create_dirs import create_dirs
from av_tasks.audio.copy_audio_masters import copy_audio_master_files
from av_tasks.audio.create_audio_checksum import create_checksum
from av_tasks.audio.save_audio_technical_metadata import save_audio_tech_md
from av_tasks.audio.get_descriptive_metadata_from_AMS import get_descriptive_metadata
from av_tasks.audio.put_technical_metadata_to_AMS import put_techmd_to_ams
from av_tasks.audio.transcode_audio_masters import transcode_audio
from av_tasks.audio.send_audio_info_mail import send_AIP_info

INPUT_DIR = os.environ.get("AUDIO_INPUT_DIR", default='/opt/av_hdd/audios')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
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

copy_audio_masters = PythonOperator(
    task_id='copy_audio_master_files_to_directory',
    python_callable=copy_audio_master_files,
    dag=audio_workflow
)

create_checksum_from_audio_master = PythonOperator(
    task_id='create_checksum_from_audio_master_file',
    python_callable=create_checksum,
    dag=audio_workflow
)

save_audio_technical_metadata_from_audio_master = PythonOperator(
    task_id='save_audio_technical_metadata_from_audio_master_file',
    python_callable=save_audio_tech_md,
    dag=audio_workflow
)

get_descriptive_metadata_from_AMS_about_audio = PythonOperator(
    task_id='get_descriptive_metadata_from_AMS_about_audio_master_file',
    python_callable=get_descriptive_metadata,
    dag=audio_workflow
)

put_technical_metadata_to_AMS_from_audio = PythonOperator(
    task_id='put_technical_metadata_to_AMS_from_audio_master_file',
    python_callable=put_techmd_to_ams,
    dag=audio_workflow
)

transcode_audio_master = PythonOperator(
    task_id='transcode_audio_master_file',
    python_callable=transcode_audio,
    dag=audio_workflow
)

send_AIP_info_mail = PythonOperator(
    task_id='sending_aip_info_email',
    python_callable=send_AIP_info,
    dag=audio_workflow,
    trigger_rule='one_success'
)


def triggering_dag(context, dag_run_obj):
    if any(os.listdir(INPUT_DIR)):
        return dag_run_obj
    else:
        return None


retrigger_dag = TriggerDagRunOperator(
    task_id='rerun_DAG',
    trigger_dag_id='audio-workflow',
    python_callable=triggering_dag,
    dag=audio_workflow)

# Flow
collect_audio_files.set_downstream(check_barcode_existence)
check_barcode_existence.set_downstream(create_dirs)
create_dirs.set_downstream(copy_audio_masters)
copy_audio_masters.set_downstream(create_checksum_from_audio_master)
create_checksum_from_audio_master.set_downstream(save_audio_technical_metadata_from_audio_master)
save_audio_technical_metadata_from_audio_master.set_downstream(get_descriptive_metadata_from_AMS_about_audio)
get_descriptive_metadata_from_AMS_about_audio.set_downstream(put_technical_metadata_to_AMS_from_audio)
put_technical_metadata_to_AMS_from_audio.set_downstream(transcode_audio_master)
transcode_audio_master.set_downstream(send_AIP_info_mail)
send_AIP_info_mail.set_downstream(retrigger_dag)
