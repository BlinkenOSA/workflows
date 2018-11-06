import json
import os
import requests
import logging

from datetime import datetime
from airflow.utils.email import send_email


log = logging.getLogger(__name__)

OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/output')
VIDEO_LIST = os.path.join(OUTPUT_DIR, 'videofiles.json')
AMS_API = os.environ.get("AMS_API", default='http://ams.osaarchivum.org/api/')
AMS_API_TOKEN = os.environ.get("AMS_API_TOKEN", default='<api_token>')
AV_STAFF_EMAIL_LIST = os.environ.get("AV_STAFF_EMAIL_LIST", default='')


def push_to_ams():
    if not os.path.exists(VIDEO_LIST):
        log.error("Video list file '%s' doesn't exists" % VIDEO_LIST)
        raise Exception

    with open(VIDEO_LIST, 'r') as video_list_file:
        video_list = json.load(video_list_file)

    for barcode, path in video_list.items():
        barcode_dir = os.path.join(OUTPUT_DIR, barcode)
        metadata_dir = os.path.join(barcode_dir, 'Metadata', 'Preservation')
        metadata_file = os.path.join(metadata_dir, "%s_md_tech.json" % barcode)

        with open(metadata_file, 'r') as metadata:
            technical_metadata = metadata.read()

        headers = {"Authorization": "Bearer %s" % AMS_API_TOKEN}
        data = {
            'barcode': barcode,
            'digital_version_exists': True,
            'digital_version_technical_metadata': technical_metadata,
            'digital_version_creation_date': datetime.now().strftime('%Y-%m-%d')
        }
        url = "%s/%s/%s/" % (AMS_API, 'containers', barcode)
        log.info("Pushing metadata through %s" % url)
        r = requests.put(url=url, data=data, headers=headers)
        if r.status_code == 200:
            log.info("OK - Data ingested to AMS...")
        elif r.status_code == 404:
            log.info("Sending notification email...")
            email_title = "AV Digitization Workflow - Missing Barcode: %s" % barcode
            email_body = """
            Dear AV team, <br>
            <br>
            It seems that the barcode %s is not registered in the AMS. Please give it a look! <br>
            Your sincerely,<br>
            AV workflow<br>
            """ % barcode
            emails = AV_STAFF_EMAIL_LIST.split(',')
            send_email(emails, email_title, email_body)
        else:
            log.error("Bad request to: %s" % r.url)
            log.error("Response: %s - %s" % (r.status_code, r.reason))
            log.error("Error message: %s" % r.content)
            raise Exception


if __name__ == '__main__':
    push_to_ams()