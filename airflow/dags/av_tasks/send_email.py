import os
from airflow.utils.email import send_email


AV_STAFF_EMAIL_LIST = os.environ.get('AV_STAFF_EMAIL_LIST', default=[])


def notify_email(contextDict, **kwargs):
        
    email_title = "Airflow task: {task_name}".format(**contextDict)
    
    email_body = """
    Dear AV team, <br>
    <br>
    The task {task_name} has been finished, and done <br>
    Your sincerely,<br>
    AV workflow<br>
    """.format(**contextDict)
    emails = AV_STAFF_EMAIL_LIST.split(',')
    send_email(emails, email_title, email_body)
