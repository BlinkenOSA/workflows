import json

# from config import INPUT_DIR, OUTPUT_DIR, VIDEO_LIST
from python_tasks.config import INPUT_DIR, OUTPUT_DIR, VIDEO_LIST
from pathlib import Path


def main():
    collect_files()


def collect_files():
    print("Collecting files from %s" % INPUT_DIR)
    file_list = {}
    barcode = ""

    pathlist = Path(INPUT_DIR).glob('**/*.avi')
    for path in pathlist:
        file_name = str(path.name).strip('.avi')
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
    main()
