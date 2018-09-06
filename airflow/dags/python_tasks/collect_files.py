import json

import pathlib

from .config import INPUT_DIR, OUTPUT_DIR, VIDEO_LIST, FILE_EXTENSION
from pathlib import Path


def collect_files():
    print("Generate output directory %s" % OUTPUT_DIR)
    pathlib.Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    print("Collecting files from %s" % INPUT_DIR)
    file_list = {}
    barcode = ""

    pathlist = list(Path(INPUT_DIR).glob('**/*.%s' % FILE_EXTENSION))
    if len(pathlist) > 0:
        path = pathlist[0]
    else:
        print("Directory doesn't contain files with extension: %s" % FILE_EXTENSION)
        raise Exception

    file_name = str(path.name).strip('.%s' % FILE_EXTENSION)
    if is_number(file_name):
        barcode = file_name
    else:
        parent_dir = path.parts[len(path.parts)-2]
        if is_number(parent_dir):
            barcode = parent_dir

    if barcode == "":
        print("No barcode can be found in %s" % str(path))
    else:
        file_list[barcode] = str(path)

    if len(file_list) > 0:
        with open(VIDEO_LIST, 'w') as outfile:
            json.dump(file_list, outfile)
            print("List of video files were created in %s" % VIDEO_LIST)
    else:
        print("No video can be found in %s" % INPUT_DIR)
        raise Exception


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    collect_files()
