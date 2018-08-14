import os
import json
import pathlib

# from config import INPUT_DIR, OUTPUT_DIR, VIDEO_LIST
from python_tasks.config import INPUT_DIR, OUTPUT_DIR, VIDEO_LIST


def main():
    craete_directories()


def craete_directories():
    if not os.path.exists(VIDEO_LIST):
        print("Video list file '%s' doesn't exists" % VIDEO_LIST)
        raise Exception

    with open(VIDEO_LIST, 'r') as video_list_file:
        video_list = json.load(video_list_file)

        for barcode, path in video_list.items():
            barcode_dir = os.path.join(OUTPUT_DIR, 'OSA-AIP_%s' % barcode)
            pathlib.Path(barcode_dir).mkdir(parents=True, exist_ok=True)

            pathlib.Path(os.path.join(barcode_dir, 'Content', 'Preservation')).mkdir(parents=True, exist_ok=True)
            pathlib.Path(os.path.join(barcode_dir, 'Content', 'Access')).mkdir(parents=True, exist_ok=True)
            pathlib.Path(os.path.join(barcode_dir, 'Metadata', 'Preservation')).mkdir(parents=True, exist_ok=True)
            pathlib.Path(os.path.join(barcode_dir, 'Metadata', 'Access')).mkdir(parents=True, exist_ok=True)

            print("Directory '%s' was created" % barcode_dir)

if __name__ == '__main__':
    main()