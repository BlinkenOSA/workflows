import json
import os
import logging
import docker

log = logging.getLogger(__name__)

OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/output')
VIDEO_LIST = os.path.join(OUTPUT_DIR, 'videofiles.json')
MASTER_FILE_EXTENSION = os.environ.get("AV_MASTER_FILE_EXTENSION", default='mpg')
ACCESS_FILE_EXTENSION = os.environ.get("AV_ACCESS_FILE_EXTENSION", default='mp4')
WORKING_DIR = os.environ.get("AV_FINAL_DIR", default="/opt/output")


def encode_masters(on_success=None, on_error=None):
    client = docker.from_env()

    if not os.path.exists(VIDEO_LIST):
        log.error("Video list file '%s' doesn't exists" % VIDEO_LIST)
        raise Exception

    with open(VIDEO_LIST, 'r') as video_list_file:
        video_list = json.load(video_list_file)

    for barcode, path in video_list.items():
        barcode_dir = os.path.join(OUTPUT_DIR, barcode)
        master_dir = os.path.join(barcode_dir, 'Content', 'Preservation')
        access_dir = os.path.join(barcode_dir, 'Content', 'Access')
        docker_dir = '/root/data'

        input_file = os.path.join(master_dir, '%s.%s' % (barcode, MASTER_FILE_EXTENSION))
        output_file = os.path.join(access_dir, '%s.%s' % (barcode, ACCESS_FILE_EXTENSION))

        volumes = {}
        volumes[WORKING_DIR] = {'bind': docker_dir, 'mode': 'rw'}

        # Set FFMPEG params
        command = ['ffmpeg', '-hwacce', 'cuvid', '-c:v', 'h264_cuvid', '-i', input_file, '-c:v', 'h264_nvenc', output_file]

        # Run ffmpeg in docker container
        try:
            client.containers.run(
                image="nightseas/ffmpeg",
                command=" ".join(command),
                volumes=volumes
            )
            return on_success
        except docker.errors.ContainerError as e:
            log.error(e.stderr)
            return on_error

if __name__ == '__main__':
    encode_masters()
