import json
import logging
import os
import pathlib

log = logging.getLogger(__name__)

OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/av_hdd/aip')
AUDIO_FILE = os.path.join(OUTPUT_DIR, 'audiofiles.json')


def create_dirs():

    with open(AUDIO_FILE, 'r') as audio_file:
        audio_file_barcode = list(json.load(audio_file))[0]

    barcode_dir = os.path.join(OUTPUT_DIR, audio_file_barcode)
    pathlib.Path(barcode_dir).mkdir(parents=True, exist_ok=True)

    pathlib.Path(os.path.join(barcode_dir, 'Content', 'Preservation')).mkdir(
        parents=True, exist_ok=True)
    pathlib.Path(os.path.join(barcode_dir, 'Content', 'Access')
                 ).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.join(barcode_dir, 'Metadata', 'Preservation')).mkdir(
        parents=True, exist_ok=True)

    log.info("'%s' directory created" % barcode_dir)


if __name__ == '__main__':
    create_dirs()
