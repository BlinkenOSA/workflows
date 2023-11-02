import json
import os
import requests
import time

OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/av_hdd/aip')
AUDIO_JSON_FILE = os.path.join(OUTPUT_DIR, 'audiofiles.json')
AMS_API = os.environ.get("AMS_API", default='https://ams-api.osaarchivum.org/v1/workflow/containers')
AMS_API_TOKEN = os.environ.get("AMS_API_TOKEN", default='<api_token>')


def put_techmd_to_ams():
    with open(AUDIO_JSON_FILE, 'r') as audio_list_file:
        audio_file = json.load(audio_list_file)

    for barcode, path in audio_file.items():
        barcode_dir = os.path.join(OUTPUT_DIR, barcode)
        metadata_dir = os.path.join(barcode_dir, 'Metadata', 'Preservation')
        metadata_file = os.path.join(metadata_dir, "%s_md_tech.json" % barcode)
        mod_time = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(metadata_file)))

        with open(metadata_file, 'r') as metadata:
            technical_metadata = metadata.read()

        headers = {"Authorization": "Bearer %s" % AMS_API_TOKEN}
        data_to_put = {
            'barcode': barcode,
            'digital_version_exists': True,
            'digital_version_technical_metadata': technical_metadata,
            'digital_version_creation_date': mod_time
        }

        url = "%s/%s/" % (AMS_API, barcode)
        r = requests.put(url=url, data=data_to_put, headers=headers, allow_redirects=True)

        if r.status_code == 200:
            print("OK - Data ingested to AMS...")
        else:
            print("Bad request to: %s" % r.url)
            print("Response: %s - %s" % (r.status_code, r.reason))
            print("Error message: %s" % r.content)
            raise Exception


if __name__ == '__main__':
    put_techmd_to_ams()
