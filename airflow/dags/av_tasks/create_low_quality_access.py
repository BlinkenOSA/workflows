import json
import os
import logging
import docker

log = logging.getLogger(__name__)

OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/output')
VIDEO_LIST = os.path.join(OUTPUT_DIR, 'videofiles.json')
ACCESS_FILE_EXTENSION = os.environ.get("AV_ACCESS_FILE_EXTENSION", default='mp4')
WORKING_DIR = os.environ.get("AV_FINAL_DIR", default="/opt/output")


def create_low_quality():
    client = docker.from_env()

    if not os.path.exists(VIDEO_LIST):
        log.error("Video list file '%s' doesn't exists" % VIDEO_LIST)
        raise Exception

    with open(VIDEO_LIST, 'r') as video_list_file:
        video_list = json.load(video_list_file)

    for barcode,path in video_list.items():
        docker_dir = '/root/data'

        volumes = {}
        volumes[os.path.join(WORKING_DIR, barcode)] = {'bind': docker_dir, 'mode': 'rw'}

        input_file = os.path.join(docker_dir, 'Content', 'Access', '%s.%s' % (barcode, ACCESS_FILE_EXTENSION))
        output_file = os.path.join(docker_dir, 'Content', 'Access', '%s-low.%s' % (barcode, ACCESS_FILE_EXTENSION))

        # Set FFMPEG params
        command = ['ffmpeg',
                   '-i', input_file,
                   '-ar', '44100',
                   '-c:v', 'h264_nvenc',
                   '-b:v', '2M',
                   '-maxrate', '2M',
                   '-bufsize', '1M',
                   '-movflags', '+faststart',
                   output_file]

        log.info("Running command '%s'" % " ".join(command))

        # Run ffmpeg in docker container
        try:
            client.containers.run(
                image="nightseas/ffmpeg",
                command=" ".join(command),
                runtime="nvidia",
                volumes=volumes
            )
        except docker.errors.ContainerError as e:
            log.error(e.stderr)

if __name__ == '__main__':
    create_low_quality()
