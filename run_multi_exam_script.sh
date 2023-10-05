#!/bin/bash
# Use -n for the number of times you want to run the Python script.
# Use -t for the text of the track to click. Take the text title of the track name.
# Run script with ./run_multi_exam_script.sh -n 5 -t "YourTrackText"

# Function to determine the operating system
detect_os() {
  case "$(uname -s)" in
    Linux*)   os="linux";;
    Darwin*)  os="macos";;
    CYGWIN*|MINGW32*|MSYS*|MINGW*) os="windows";;
    *)        os="unknown";;
  esac
}

while getopts ":n:t:" opt; do
  case $opt in
    n) num_times="$OPTARG"
    ;;
    t) track_text="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

# Determine the operating system
detect_os

# Update locators.py with the track text
if [ "$os" == "windows" ]; then
  # For Windows, use the following sed command
  sed -i "s/PLACEHOLDER/$track_text/g" multi_exam_taker.py
else
  # For Linux and macOS, use the following sed command
  sed -i'' -e "s/PLACEHOLDER/$track_text/g" multi_exam_taker.py
fi

# Loop to run the Python script n times
for i in $(seq 1 $num_times); do
   python multi_exam_taker.py
done

# Revert back to PLACEHOLDER after the loop
if [ "$os" == "windows" ]; then
  # For Windows, use the following sed command
  sed -i "s/$track_text/PLACEHOLDER/g" multi_exam_taker.py
else
  # For Linux and macOS, use the following sed command
  sed -i'' -e "s/$track_text/PLACEHOLDER/g" multi_exam_taker.py
fi
