import json
import os

import subprocess
import logging

import docker
from airflow.models import Variable

log = logging.getLogger(__name__)


OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/output')
VIDEO_LIST = os.path.join(OUTPUT_DIR, 'videofiles.json')
WORKING_DIR = os.environ.get("AV_FINAL_DIR", default="/opt/output")


def create_video_info(directory='Preservation', file_extension='mpg'):
    client = docker.from_env()

    if not os.path.exists(VIDEO_LIST):
        log.error("Video list file '%s' doesn't exists" % VIDEO_LIST)
        raise Exception

    with open(VIDEO_LIST, 'r') as video_list_file:
        video_list = json.load(video_list_file)

    for barcode, path in video_list.items():
        barcode_dir = os.path.join(OUTPUT_DIR, barcode)
        metadata_dir = os.path.join(barcode_dir, 'Metadata', directory)
        docker_dir = '/root/data'

        volumes = {}
        volumes[os.path.join(WORKING_DIR, barcode)] = {'bind': docker_dir, 'mode': 'rw'}

        # logging:
        log.info(WORKING_DIR)
        log.info("Starting ffmpeg docker, mapping %s as %s" % (os.path.join(WORKING_DIR, barcode), docker_dir))

        input_dir = os.path.join(docker_dir, 'Content', directory)
        input_file = os.path.join(input_dir, '%s.%s' % (barcode, file_extension))

        command = ['ffprobe', '-i', input_file, '-show_format', '-show_streams', '-print_format', 'json']

        # Run ffmpeg in docker container
        output = client.containers.run(
            image="nightseas/ffmpeg",
            command=" ".join(command),
            volumes=volumes
        )
        log.info("Writing technical metadata to file...")

        with open(os.path.join(metadata_dir, "%s_md_tech.json" % barcode), 'w') as metadata_file:
            metadata_file.write(output.decode('utf-8'))


if __name__ == '__main__':
    create_video_info()
