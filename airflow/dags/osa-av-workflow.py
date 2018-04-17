from datetime import timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import CreateDirectoryStructureOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['bonej@ceu.edu', 'danij@ceu.edu'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


dag = DAG('osa-av-workflow',description='Main DAG for the preservation workflow', default_args=default_args, schedule_interval=timedelta(1),catchup=False)

dummy_task = DummyOperator(task_id="dummy_task", dag=dag)

createdirectorystructureoperator_task = CreateDirectoryStructureOperator(param="Test",task_id="create_directory_structure_operator_task",dag=dag)

dummy_task >> createdirectorystructureoperator_task
