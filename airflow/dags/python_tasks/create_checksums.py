import os
import json
import hashlib

from .config import OUTPUT_DIR, VIDEO_LIST, FILE_EXTENSION

BLOCKSIZE = 65536


def create_checksums():
    if not os.path.exists(VIDEO_LIST):
        print("Video list file '%s' doesn't exists" % VIDEO_LIST)
        raise Exception

    with open(VIDEO_LIST, 'r') as video_list_file:
        video_list = json.load(video_list_file)

    for barcode, path in video_list.items():
        barcode_dir = os.path.join(OUTPUT_DIR, 'OSA-AIP_%s' % barcode)
        master_dir = os.path.join(barcode_dir, 'Content', 'Preservation')
        master_file = os.path.join(master_dir, '%s.%s' % (barcode, FILE_EXTENSION))
        hash_dir = os.path.join(barcode_dir, 'Metadata', 'Preservation')

        md5 = hashlib.md5()
        sha512 = hashlib.sha512()

        with open(master_file, 'rb') as mf:
            file_buffer = mf.read(BLOCKSIZE)
            while len(file_buffer) > 0:
                md5.update(file_buffer)
                sha512.update(file_buffer)
                file_buffer = mf.read(BLOCKSIZE)

        with open(os.path.join(hash_dir, "%s.md5" % barcode), 'w') as md5_file:
            md5_file.write(md5.hexdigest())

        with open(os.path.join(hash_dir, "%s.sha512" % barcode), 'w') as sha512_file:
            sha512_file.write(sha512.hexdigest())

if __name__ == '__main__':
    create_checksums()
