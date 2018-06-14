#!/bin/bash

#   ----------------------------------------------------------------
#   Function for transcoding master files
#       Accepts 1 argument:
#           string containing the path of the videos
#   ----------------------------------------------------------------
function do_transcoding_to_mp4()
{
    local video_directory_path=$1
    local file_extension="mp4"
    for video_files in $video_directory_path/*
    do
        # perhaps we should copy the file into a local directory first
        # first extract the filename and the extension from the path that given && then after extract only the name of it
        local video_file_name=$(basename $video_files) && video_file_name="${video_file_name%.*}"
        echo $video_file_name
    done        
}

program_name=$(basename $0)
# for further development store the argument in an array like this:
# args=("$@")
# to access them use: ${args[0] ... and so on}
if [ "$#" -ne 1 ]
then
    echo "Illegal number of parameters"    
else    
    do_transcoding_to_mp4 $1
fi