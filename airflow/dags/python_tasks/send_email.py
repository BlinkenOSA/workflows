from airflow.utils.email import send_email
from .config import AIRFLOW_STAFF_EMAIL_LIST


def notify_email(contextDict, **kwargs):
        
    email_title = "Airflow task: {task_name}".format(**contextDict)
    
    email_body = """
    Dear AV team, <br>
    <br>
    The task {task_name} has been finished, and done <br>
    Your sincerely,<br>
    AV workflow<br>
    """.format(**contextDict)

    send_email(AIRFLOW_STAFF_EMAIL_LIST, email_title, email_body)
