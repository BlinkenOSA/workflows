import os

INPUT_DIR = '/INPUT_DIR'
OUTPUT_DIR = '/OUTPUT_DIR'

MASTER_FILE_EXTENSION = 'mpg'
ACCESS_FILE_EXTENSION = 'mp4'

VIDEO_LIST = os.path.join(OUTPUT_DIR, 'videofiles.json')

FFMPEG_DIR = '/usr/local/bin/'

AMS_API = 'http://ams.osaarchivum.org/api/'
AMS_API_TOKEN = 'AMS_API_TOKEN'

BARCODE_PATTERN = '^HU_OSA_[0-9]{8}$'

AIRFLOW_STAFF_EMAIL_LIST = ['bonej@ceu.edu', 'danij@ceu.edu']
AV_STAFF_EMAIL_LIST = ['bonej@ceu.edu', 'danij@ceu.edu']