#!/bin/bash

#   ----------------------------------------------------------------
#   Function for transcoding master files
#       Accepts 1 argument:
#           string containing the path of the videos
#   ----------------------------------------------------------------
function do_transcoding_to_mp4()
{
    local video_directory_path=$1
    echo "$video_directory_path in $program_name"   
}

program_name=$(basename $0)
if [ "$#" -ne 1 ]
then
    echo "Illegal number of parameters"
else
    do_transcoding_to_mp4 $1
fi