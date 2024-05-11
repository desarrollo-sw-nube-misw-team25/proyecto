#!/bin/bash


if [ $# -ne 1 ]; then
    echo "Usage: $0 <video_path>"
    exit 1
fi

video_name="$1"
input_video="/home/pelucapreb/${video_name}"
processed_folder="/home/pelucapreb"
output_video="${processed_folder}/${video_name%.*}_processed.mp4"

sudo gsutil cp "gs://almacenamiento2-videos-nube/unprocessed/${video_name}" "${input_video}"

# Revisar si se descargo bien
if [ ! -f "$input_video" ]; then
    echo "Failed to download video."
    exit 1
fi


initial_frame="./idrl.jpg"
final_frame="./idrl.jpg"

video_width=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=s=x:p=0 "$input_video")
video_height=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=s=x:p=0 "$input_video")

# Calculate overlay position for centering
overlay_x=$((($video_width - 1920) / 2))
overlay_y=$((($video_height - 1080) / 2))

# Process the video
ffmpeg -i "$input_video" -i "$initial_frame" -i "$final_frame" \
-filter_complex "[0:v][1:v] overlay=$overlay_x:$overlay_y:enable='between(t,0,1)' [tmp]; [tmp][2:v] overlay=$overlay_x:$overlay_y:enable='between(t,19,20)'" \
-c:v libx264 -c:a copy -t 20 "$output_video"

echo "The processed video has been saved as: $output_video"

sudo gsutil cp "sudo ${output_video}" "gs://almacenamiento2-videos-nube/processed/" 

rm -f "$input_video"
rm -f "$output_video"

echo "Local copies of videos have been deleted."
