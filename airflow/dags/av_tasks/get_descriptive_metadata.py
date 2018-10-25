import json
import os
import requests
import logging

from airflow.models import Variable

log = logging.getLogger(__name__)

OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/output')
VIDEO_LIST = os.path.join(OUTPUT_DIR, 'videofiles.json')

AMS_API = os.environ.get("AMS_API", default='http://ams.osaarchivum.org/api/')
AMS_API_TOKEN = os.environ.get("AMS_API_TOKEN", default='<api_token>')


def get_descriptive_metadata():
    if not os.path.exists(VIDEO_LIST):
        log.error("Video list file '%s' doesn't exists" % VIDEO_LIST)
        raise Exception

    with open(VIDEO_LIST, 'r') as video_list_file:
        video_list = json.load(video_list_file)

    for barcode, path in video_list.items():
        barcode_dir = os.path.join(OUTPUT_DIR, barcode)
        metadata_dir = os.path.join(barcode_dir, 'Metadata', 'Preservation')
        metadata_file = os.path.join(metadata_dir, "%s_md_descriptive.json" % barcode)

        headers = {"Authorization": "Bearer %s" % AMS_API_TOKEN}
        url = "%s/%s/%s/" % (AMS_API, 'containers/metadata', barcode)
        log.info("Trying to fetch metadata from: %s" % url)
        r = requests.get(url=url, headers=headers)

        if r.status_code == 200:
            with open(metadata_file, 'w') as metadata:
                metadata.write(json.dumps(r.json()['results']))
                log.info("OK - Descriptive metadata collected...")
        else:
            log.error("Bad request to: %s" % r.url)
            log.error("Response: %s - %s" % (r.status_code, r.reason))


if __name__ == '__main__':
    get_descriptive_metadata()
