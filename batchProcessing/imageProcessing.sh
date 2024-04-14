#!/bin/bash


if [ $# -ne 1 ]; then
    echo "Usage: $0 <input_image>"
    exit 1
fi


input_image="$1"



output_image="$input_image"



ffmpeg -i "$input_image" -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" "$output_image"

echo "Resized image saved as: $output_image"
