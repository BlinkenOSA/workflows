import json
import logging
import os
import pathlib
import re

from pathlib import Path

log = logging.getLogger(__name__)

INPUT_DIR = os.environ.get("AUDIO_INPUT_DIR", default='/opt/av_hdd/audios')
OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/av_hdd/aip')
AUDIO_FILE_LIST = os.path.join(OUTPUT_DIR, 'audiofiles.json')
AUDIO_MASTER_FILE_EXTENSION = os.environ.get(
    "AUDIO_MASTER_FILE_EXTENSION", default='wav')
BARCODE_PATTERN = os.environ.get(
    'AV_BARCODE_PATTERN', default='^HU_OSA_[0-9]{8}$')


def collect_audio_files():
    log.info("Generate output directory %s" % OUTPUT_DIR)
    pathlib.Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    log.info("Collecting files from %s" % INPUT_DIR)
    file_list = {}
    barcode = ""

    pathlist = list(Path(INPUT_DIR).glob('**/*.%s' %
                    AUDIO_MASTER_FILE_EXTENSION))
    if len(pathlist) > 0:
        path = pathlist[0]
    else:
        log.error("Directory doesn't contain files with extension: %s" %
                  AUDIO_MASTER_FILE_EXTENSION)
        raise Exception

    # XXX: this part needs refactorization
    file_name = str(path.name).strip('.%s' % AUDIO_MASTER_FILE_EXTENSION)
    if re.match(BARCODE_PATTERN, file_name):
        barcode = file_name
    else:
        parent_dir = path.parts[len(path.parts)-2]
        if re.match(BARCODE_PATTERN, parent_dir):
            barcode = parent_dir

    if barcode == "":
        log.error("No barcode can be found in %s" % str(path))
        raise Exception
    else:
        file_list[barcode] = str(path)

    if len(file_list) > 0:
        with open(AUDIO_FILE_LIST, 'w') as outfile:
            json.dump(file_list, outfile)
            log.info("List of video files were created in %s" %
                     AUDIO_FILE_LIST)

    # FIXME: no need (see line 30-35)
    else:
        log.error("No audio file can be found in %s" % INPUT_DIR)
        raise Exception


if __name__ == '__main__':
    collect_audio_files()
