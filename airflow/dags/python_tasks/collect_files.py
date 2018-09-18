import json
import logging
import pathlib

import re

from .config import INPUT_DIR, OUTPUT_DIR, VIDEO_LIST, MASTER_FILE_EXTENSION, BARCODE_PATTERN
from pathlib import Path

log = logging.getLogger(__name__)


def collect_files():
    log.info("Generate output directory %s" % OUTPUT_DIR)
    pathlib.Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    log.info("Collecting files from %s" % INPUT_DIR)
    file_list = {}
    barcode = ""

    pathlist = list(Path(INPUT_DIR).glob('**/*.%s' % MASTER_FILE_EXTENSION))
    if len(pathlist) > 0:
        path = pathlist[0]
    else:
        log.error("Directory doesn't contain files with extension: %s" % MASTER_FILE_EXTENSION)
        raise Exception

    file_name = str(path.name).strip('.%s' % MASTER_FILE_EXTENSION)
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
        with open(VIDEO_LIST, 'w') as outfile:
            json.dump(file_list, outfile)
            log.info("List of video files were created in %s" % VIDEO_LIST)
    else:
        log.error("No video can be found in %s" % INPUT_DIR)
        raise Exception


if __name__ == '__main__':
    collect_files()
