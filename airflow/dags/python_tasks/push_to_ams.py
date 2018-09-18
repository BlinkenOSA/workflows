import json
import os
import requests
import logging

from datetime import datetime

from .config import OUTPUT_DIR, VIDEO_LIST, AMS_API, AMS_API_TOKEN

log = logging.getLogger(__name__)


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
            'digital_version_creation_date': datetime.now()
        }

        r = requests.put(url="%s%s/%s/" % (AMS_API, 'containers', barcode), data=data, headers=headers)
        if r.status_code == '200':
            log.info("OK - Data ingested to AMS...")
        else:
            log.error("Bad request to: %s" % r.url)
            log.error("Response: %s - %s" % (r.status_code, r.reason))


if __name__ == '__main__':
    push_to_ams()