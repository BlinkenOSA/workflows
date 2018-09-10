import json
import os
import requests

from .config import OUTPUT_DIR, VIDEO_LIST, AMS_API, AMS_API_TOKEN


def push_to_ams():
    if not os.path.exists(VIDEO_LIST):
        print("Video list file '%s' doesn't exists" % VIDEO_LIST)
        raise Exception

    with open(VIDEO_LIST, 'r') as video_list_file:
        video_list = json.load(video_list_file)

    for barcode, path in video_list.items():
        barcode_dir = os.path.join(OUTPUT_DIR, 'OSA-AIP_%s' % barcode)
        metadata_dir = os.path.join(barcode_dir, 'Metadata', 'Preservation')
        metadata_file = os.path.join(metadata_dir, "%s_md_tech.json" % barcode)

        with open(metadata_file, 'r') as metadata:
            technical_metadata = metadata.read()

        headers = {"Authorization": "Bearer %s" % AMS_API_TOKEN}
        data = {
            'barcode': barcode,
            'digital_version_exists': True,
            'technical_metadata': technical_metadata
        }

        r = requests.put(url="%s%s/%s/" % (AMS_API, 'containers', barcode), data=data, headers=headers)
        if r.status_code == '200':
            print("OK")
        else:
            print("Bad request to: %s" % r.url)
            print("Response: %s - %s" % (r.status_code, r.reason))


if __name__ == '__main__':
    push_to_ams()