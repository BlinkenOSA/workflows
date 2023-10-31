import json
import os
import requests
import logging

log = logging.getLogger(__name__)

OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/av_hdd/aip')
AUDIO_JSON_FILE = os.path.join(OUTPUT_DIR, 'audiofiles.json')
AMS_API = os.environ.get("AMS_API", default='https://ams-api.osaarchivum.org/v1/workflow/containers')
AMS_API_TOKEN = os.environ.get("AMS_API_TOKEN", default='<api_token>')


def get_descriptive_metadata():
    with open(AUDIO_JSON_FILE, 'r') as audio_list_file:
        audio_file = json.load(audio_list_file)

    for barcode, path in audio_file.items():
        barcode_dir = os.path.join(OUTPUT_DIR, barcode)
        metadata_dir = os.path.join(barcode_dir, 'Metadata', 'Preservation')
        metadata_file = os.path.join(metadata_dir, "%s_md_descriptive.json" % barcode)

        headers = {"Authorization": "Bearer %s" % AMS_API_TOKEN}
        url = "%s/%s/%s" % (AMS_API, 'metadata', barcode)
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
