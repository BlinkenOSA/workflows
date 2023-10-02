import json
import os
import docker


OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/av_hdd/aip')
AUDIO_LIST = os.path.join(OUTPUT_DIR, 'audiofiles.json')


def save_audio_tech_md(directory='Preservation', file_extension='wav'):
    client = docker.from_env()

    with open(AUDIO_LIST, 'r') as audio_list_file:
        audio_file = json.load(audio_list_file)

    for barcode, path in audio_file.items():
        barcode_dir = os.path.join(OUTPUT_DIR, barcode)
        metadata_dir = os.path.join(barcode_dir, 'Metadata', directory)
        docker_dir = '/root/data'
        volumes = {}
        volumes[os.path.join(OUTPUT_DIR, barcode)] = {
            'bind': docker_dir, 'mode': 'rw'}

        input_dir = os.path.join(docker_dir, 'Content', directory)
        input_file = os.path.join(input_dir, '%s.%s' %
                                  (barcode, file_extension))

        command = ['ffprobe', '-i', input_file, '-show_format',
                   '-show_streams', '-print_format', 'json']

        # Run ffmpeg in docker container
        output = client.containers.run(
            image="nightseas/ffmpeg",
            command=" ".join(command),
            volumes=volumes
        )

        with open(os.path.join(metadata_dir, "%s_md_tech.json" % barcode), 'w') as metadata_file:
            metadata_file.write(output.decode('utf-8'))


if __name__ == '__main__':
    save_audio_tech_md()
