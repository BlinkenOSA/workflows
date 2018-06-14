#!/bin/bash

#   ----------------------------------------------------------------
#   Function for transcoding master files
#       Accepts 1 argument:
#           string containing the path of the videos
#   ----------------------------------------------------------------
function do_transcoding_to_mp4()
{
    file_extension="mp4"
    local video_directory_path=$1
    for video_files in $video_directory_path/*
    do
        echo $video_files
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