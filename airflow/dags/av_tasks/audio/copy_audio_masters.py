import os
import json
import logging
import shutil


log = logging.getLogger(__name__)


OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/av_hdd/aip')
AUDIO_FILE = os.path.join(OUTPUT_DIR, 'audiofiles.json')
AUDIO_MASTER_FILE_EXTENSION = os.environ.get(
    "AUDIO_MASTER_FILE_EXTENSION", default='wav')


def copy_audio_master_files():

    with open(AUDIO_FILE, 'r') as audio_file:
        audio_file_to_copy = json.load(audio_file)

    for barcode, path in audio_file_to_copy.items():
        barcode_dir = os.path.join(OUTPUT_DIR, barcode)
        master_dir = os.path.join(barcode_dir, 'Content', 'Preservation')
        master_file = os.path.join(master_dir, '%s.%s' % (
            barcode, AUDIO_MASTER_FILE_EXTENSION))

        log.info("Start moving '%s'" % path)
        shutil.move(path, master_file)
        log.info("Finished moving file to '%s'" % master_file)


if __name__ == '__main__':
    copy_audio_master_files()
