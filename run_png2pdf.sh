#!/bin/bash

# Check if user has provided a directory path
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory_path>"
    exit 1
fi

directory_path="$1"

# Ensure the provided path exists and is a directory
if [ ! -d "$directory_path" ]; then
    echo "Error: $directory_path is not a directory or doesn't exist."
    exit 1
fi

# Loop through all folders in the directory
for folder in "$directory_path"/*; do
    if [ -d "$folder" ]; then
        echo "$folder"  # Print the directory path of the sub-folder
    fi
done

echo "All folders processed."
