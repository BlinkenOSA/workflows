from airflow.utils.email import send_email

def notify_email(contextDict, **kwargs):
        
    email_title = "Airflow task: {task_name}".format(**contextDict)
    
    email_body = """
    Dear AV team, <br>
    <br>
    The task {task_name} has been finished, and done <br>
    Your sincerely,<br>
    AV workflow<br>
    """.format(**contextDict)

    send_email('bonej@ceu.edu', email_title, email_body)
