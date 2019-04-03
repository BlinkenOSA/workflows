import os
import json
import logging
import shutil


log = logging.getLogger(__name__)


OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/output')
VIDEO_LIST = os.path.join(OUTPUT_DIR, 'videofiles.json')
MASTER_FILE_EXTENSION = os.environ.get("AV_MASTER_FILE_EXTENSION", default='avi')


def copy_master_files():
    if not os.path.exists(VIDEO_LIST):
        log.error("Video list file '%s' doesn't exists" % VIDEO_LIST)
        raise Exception

    with open(VIDEO_LIST, 'r') as video_list_file:
        video_list = json.load(video_list_file)

    for barcode, path in video_list.items():
        barcode_dir = os.path.join(OUTPUT_DIR, barcode)
        master_dir = os.path.join(barcode_dir, 'Content', 'Preservation')
        master_file = os.path.join(master_dir, '%s.%s' % (barcode, MASTER_FILE_EXTENSION))

        log.info("Start moving '%s'" % path)
        shutil.move(path, master_file)
        log.info("Finished moving file to '%s'" % master_file)

if __name__ == '__main__':
    copy_master_files()