import json
import os
import requests
import logging

from airflow.utils.email import send_email

log = logging.getLogger(__name__)

OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/av_hdd/aip')
AUDIO_FILE = os.path.join(OUTPUT_DIR, 'audiofiles.json')
AMS_API = os.environ.get("AMS_API", default='https://ams-api.osaarchivum.org/v1/workflow/containers')
AMS_API_TOKEN = os.environ.get("AMS_API_TOKEN", default='<api_token>')
AV_STAFF_EMAIL_LIST = os.environ.get("AV_STAFF_EMAIL_LIST", default='')


def check_barcode():
    with open(AUDIO_FILE, 'r') as audio_file:
        audio_file_to_check = list(json.load(audio_file))[
            0]  # this resolves to a barcode

    headers = {"Authorization": "Bearer %s" % AMS_API_TOKEN}
    url = "%s/%s/%s" % (AMS_API, 'metadata', audio_file_to_check)
    r = requests.get(url=url, headers=headers)

    if r.status_code == 200:
        log.info("OK - Barcode exists!")  # Flow must go on!
    else:
        log.error("Barcode does not exists on AMS!")
        log.info("Sending notification email...")
        email_title = "AV Digitization Workflow - Missing Barcode: %s" % audio_file_to_check
        email_body = """
        Dear AV team, <br>
        <br>
        It seems that the barcode %s is not registered in the AMS. Please give it a look! <br>
        Your sincerely,<br>
        AV workflow<br>
        """ % audio_file_to_check
        emails = AV_STAFF_EMAIL_LIST.split(',')
        send_email(emails, email_title, email_body)
        raise Exception
        # TODO: set downstream to failed, shortcircuitoperator


if __name__ == '__main__':
    check_barcode()
