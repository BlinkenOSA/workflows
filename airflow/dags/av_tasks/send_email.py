import json
import os
import logging

from airflow.utils.email import send_email


log = logging.getLogger(__name__)

OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/output')
VIDEO_LIST = os.path.join(OUTPUT_DIR, 'videofiles.json')
AV_STAFF_EMAIL_LIST = os.environ.get('AV_STAFF_EMAIL_LIST', default=[])


def notify_email():
    barcodes = []

    if not os.path.exists(VIDEO_LIST):
        log.error("Video list file '%s' doesn't exists" % VIDEO_LIST)
        raise Exception

    with open(VIDEO_LIST, 'r') as video_list_file:
        video_list = json.load(video_list_file)

    for barcode, path in video_list.items():
        barcodes.append(barcode)

    if len(barcodes) > 1:
        email_title = "Task with videos %s has been finished!" % ", ".join(barcodes)
    else:
        email_title = "Task with video %s has been finished!" % barcodes[0]

    email_body = """
    Dear AV team, <br>
    <br>
    Archival Information Package for the following videos are ready:<br/><br/>
    <i>%s</i><br/><br/>
    Your sincerely,<br>
    AV workflow<br>
    """ % "<br/>".join(barcodes)

    emails = AV_STAFF_EMAIL_LIST.split(',')
    send_email(emails, email_title, email_body)
