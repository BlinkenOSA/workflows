import json
import os

import subprocess
import logging

from .config import OUTPUT_DIR, VIDEO_LIST, FFMPEG_DIR

log = logging.getLogger(__name__)


def create_video_info(directory='Preservation', file_extension='mpg'):
    if not os.path.exists(VIDEO_LIST):
        log.error("Video list file '%s' doesn't exists" % VIDEO_LIST)
        raise Exception

    with open(VIDEO_LIST, 'r') as video_list_file:
        video_list = json.load(video_list_file)

    for barcode, path in video_list.items():
        barcode_dir = os.path.join(OUTPUT_DIR, 'OSA-AIP_%s' % barcode)
        input_dir = os.path.join(barcode_dir, 'Content', directory)
        input_file = os.path.join(input_dir, '%s.%s' % (barcode, file_extension))
        metadata_dir = os.path.join(barcode_dir, 'Metadata', directory)

        args = [os.path.join(FFMPEG_DIR, 'ffprobe'), '-show_format', '-show_streams', '-of', 'json', input_file]
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            log.error(err)
            raise Error('ffprobe', out, err)

        with open(os.path.join(metadata_dir, "%s_md_tech.json" % barcode), 'w') as metadata_file:
            metadata_file.write(out.decode('utf-8'))


class Error(Exception):
    def __init__(self, cmd, stdout, stderr):
        super(Error, self).__init__('{} error (see stderr output for detail)'.format(cmd))
        self.stdout = stdout
        self.stderr = stderr


if __name__ == '__main__':
    create_video_info()