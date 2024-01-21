import json
import os
from airflow.utils.email import send_email

OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/av_hdd/aip')
AUDIO_JSON_FILE = os.path.join(OUTPUT_DIR, 'audiofiles.json')
AV_STAFF_EMAIL_LIST = os.environ.get('AV_STAFF_EMAIL_LIST', default=[])


def send_AIP_info():

    with open(AUDIO_JSON_FILE, 'r') as audio_list_file:
        audio_file = json.load(audio_list_file)

    for barcode, path in audio_file.items():
        email_title = "The AIP with audio %s has been finished!" % barcode

        email_body = """
        Dear AV team,
        <br/><br/>
        The Archival Information Package for the following audio barcode is ready:
        <br/><br/>
        <b>%s</b>
        <br/><br/>
        Your sincerely,<br/>
        AV workflow server<br/>
        """ % (barcode)

        emails = AV_STAFF_EMAIL_LIST.split(',')
        send_email(emails, email_title, email_body)


if __name__ == '__main__':
    send_AIP_info()
