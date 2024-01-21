import json
import os
import docker

OUTPUT_DIR = os.environ.get("AV_OUTPUT_DIR", default='/opt/av_hdd/aip')
AUDIO_JSON_FILE = os.path.join(OUTPUT_DIR, 'audiofiles.json')
MASTER_FILE_EXTENSION = os.environ.get("AUDIO_MASTER_FILE_EXTENSION", default='wav')
ACCESS_FILE_EXTENSION = os.environ.get("AUDIO_ACCESS_FILE_EXTENSION", default='mp3')


def transcode_audio():

    with open(AUDIO_JSON_FILE, 'r') as audio_list_file:
        audio_file = json.load(audio_list_file)

    for barcode, path in audio_file.items():

        # Define the input and output directories
        input_directory = '/opt/av_hdd/aip/%s/Content/Preservation' % (barcode)
        output_directory = '/opt/av_hdd/aip/%s/Content/Access' % (barcode)
        input_file = os.path.join(input_directory, '%s.%s' % (barcode, MASTER_FILE_EXTENSION))
        output_file = os.path.join(output_directory, '%s.%s' % (barcode, ACCESS_FILE_EXTENSION))

        # Define the FFmpeg command parameters for WAV to MP3 conversion
        # audio quality range is 0-9 where a lower value is a higher quality.
        # read more in the docs: https://trac.ffmpeg.org/wiki/Encode/MP3
        audio_quality = '2'
        ffmpeg_command = [
            '-i', input_file,
            '-codec:a', 'libmp3lame',
            '-q:a', audio_quality,
            output_file]

        client = docker.from_env()

        # Run the FFmpeg command within the linuxserver/ffmpeg container
        container = client.containers.run(
            'linuxserver/ffmpeg',
            command=ffmpeg_command,
            remove=True,  # Automatically remove the container when it exits
            detach=True,  # Run the container in the background
            volumes={
                # Mount input directory read-only
                input_directory: {'bind': input_directory, 'mode': 'ro'},
                # Mount output directory read-write
                output_directory: {'bind': output_directory, 'mode': 'rw'}
                }
        )

        # Wait for the container to finish and print its output
        # exit_code, output = container.wait(), container.logs()
        # print(f"Exit Code: {exit_code}")
        # print(f"Container Output:\n{output.decode('utf-8')}")


if __name__ == '__main__':
    transcode_audio()
