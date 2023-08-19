#!/bin/bash
# Use -n for the number of times you want to run the Python script.
# Use -t for the text of the track to click. Take the text title of the track name.
# Run script with ./run_multi_exam_script.sh -n 5 -t "YourTrackText"

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

# Update locators.py with the track text
sed -i "s/PLACEHOLDER/$track_text/g" multi_exam_taker.py

# Loop to run the Python script n times
for i in $(seq 1 $num_times);
do
   python multi_exam_taker.py
done

# Revert back to PLACEHOLDER after the loop
sed -i "s/$track_text/PLACEHOLDER/g" multi_exam_taker.py