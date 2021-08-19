import os
import json
import hashlib
import logging

from airflow.models import Variable

BLOCKSIZE = 65536

log = logging.getLogger(__name__)

OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/output')
VIDEO_LIST = os.path.join(OUTPUT_DIR, 'videofiles.json')


def create_checksums(directory='Preservation', file_extension='mp4'):
    if not os.path.exists(VIDEO_LIST):
        log.error("Video list file '%s' doesn't exists" % VIDEO_LIST)
        raise Exception

    with open(VIDEO_LIST, 'r') as video_list_file:
        video_list = json.load(video_list_file)

    for barcode, path in video_list.items():
        barcode_dir = os.path.join(OUTPUT_DIR, barcode)
        input_dir = os.path.join(barcode_dir, 'Content', directory)
        input_file = os.path.join(input_dir, '%s.%s' % (barcode, file_extension))
        hash_dir = os.path.join(barcode_dir, 'Metadata', directory)

        sha512 = hashlib.sha512()

        with open(input_file, 'rb') as mf:
            file_buffer = mf.read(BLOCKSIZE)
            while len(file_buffer) > 0:
                sha512.update(file_buffer)
                file_buffer = mf.read(BLOCKSIZE)

        with open(os.path.join(hash_dir, "%s.sha512" % barcode), 'w') as sha512_file:
            sha512_file.write(sha512.hexdigest())

if __name__ == '__main__':
    create_checksums()
