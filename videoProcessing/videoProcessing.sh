#!/bin/bash

# Revisar si el argumento es entregado
if [ $# -ne 1 ]; then
    echo "Uso: $0 <ruta del video>"
    exit 1
fi

input_video="$1"

# Nombre final del archivo
output_video="${input_video%.*}_Procesado.mp4"


initial_frame="./idrl.jpg"
final_frame="./idrl.jpg"

video_width=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=s=x:p=0 "$input_video")
video_height=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=s=x:p=0 "$input_video")

# Calculate overlay position for centering
overlay_x=$((($video_width - 1920) / 2))
overlay_y=$((($video_height - 1080) / 2))

ffmpeg -i "$input_video" -i "$initial_frame" -i "$final_frame" \
-filter_complex "[0:v][1:v] overlay=$overlay_x:$overlay_y:enable='between(t,0,1)' [tmp]; [tmp][2:v] overlay=$overlay_x:$overlay_y:enable='between(t,19,20)'" \
-c:v libx264 -c:a copy -t 20 "$output_video"

echo "EL video procesado fue guardado con el nombre: $output_video"
