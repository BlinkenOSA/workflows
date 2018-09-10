import json
import os
import ffmpeg
import logging

from .config import OUTPUT_DIR, VIDEO_LIST, MASTER_FILE_EXTENSION, ACCESS_FILE_EXTENSION, FFMPEG_DIR

log = logging.getLogger(__name__)


def encode_masters(on_success=None, on_error=None):
    with open(VIDEO_LIST, 'r') as video_list_file:
        video_list = json.load(video_list_file)

    for barcode, path in video_list.items():
        barcode_dir = os.path.join(OUTPUT_DIR, 'OSA-AIP_%s' % barcode)
        master_dir = os.path.join(barcode_dir, 'Content', 'Preservation')
        master_file = os.path.join(master_dir, '%s.%s' % (barcode, MASTER_FILE_EXTENSION))

        access_dir = os.path.join(barcode_dir, 'Content', 'Access')
        access_file = os.path.join(access_dir, '%s.%s' % (barcode, ACCESS_FILE_EXTENSION))

        ffmpeg_params = {
            'c:v': 'libx264',
            'pix_fmt': 'yuv420p',
            'crf': 34,
            'movflags': '+faststart',
            'c:a': 'aac',
            'strict': 2
        }

        try:
            (
                ffmpeg
                .input(master_file)
                .output(access_file, **ffmpeg_params)
                .overwrite_output()
                .run(cmd=os.path.join(FFMPEG_DIR, 'ffmpeg'), capture_stdout=True, capture_stderr=True)
            )
            return on_success
        except ffmpeg.Error as e:
            log.error(e.stderr)
            return on_error


if __name__ == '__main__':
    encode_masters()