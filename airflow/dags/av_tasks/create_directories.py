import os
import json
import pathlib
import logging

from airflow.models import Variable

log = logging.getLogger(__name__)


OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/output')
VIDEO_LIST = os.path.join(OUTPUT_DIR, 'videofiles.json')


def create_directories():
    if not os.path.exists(VIDEO_LIST):
        log.error("Video list file '%s' doesn't exists" % VIDEO_LIST)
        raise Exception

    with open(VIDEO_LIST, 'r') as video_list_file:
        video_list = json.load(video_list_file)

    for barcode, path in video_list.items():
        barcode_dir = os.path.join(OUTPUT_DIR, barcode)
        pathlib.Path(barcode_dir).mkdir(parents=True, exist_ok=True)

        pathlib.Path(os.path.join(barcode_dir, 'Content', 'Preservation')).mkdir(parents=True, exist_ok=True)
        pathlib.Path(os.path.join(barcode_dir, 'Content', 'Access')).mkdir(parents=True, exist_ok=True)
        pathlib.Path(os.path.join(barcode_dir, 'Metadata', 'Preservation')).mkdir(parents=True, exist_ok=True)

        log.info("Directory '%s' was created" % barcode_dir)

if __name__ == '__main__':
    create_directories()
