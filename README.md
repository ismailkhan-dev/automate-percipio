# Automate-Percipio

Automate-Percipio is a Python-based web automation project designed to help you efficiently tackle multiple-choice exams on the Percipio platform using Selenium. This repository provides a set of scripts to automate various tasks, primarily serving as a web automation bot for navigating and interacting with the Percipio platform.

## Installation

To get started with Automate-Percipio, follow these steps:

1. Clone this repository to your local machine.

    ```bash
    git clone https://github.com/ismailkhan-dev/automate-percipio.git
    ```

2. Install the necessary dependencies. You can typically do this using pip:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a file called `secret.py` in the root directory of the project. In this file, provide your Percipio login credentials:

    ```python
    USERNAME = "your_username"
    PASSWORD = "your_password"
    ```

4. Grant execute permissions to the shell scripts in the repository. Use the following command for each script you intend to use (replace `filename` with the actual script name):

    ```bash
    chmod +x filename
    ```

## Running the Exam Taker Script

Automate-Percipio offers two exam taker scripts to cater to your needs:

1. **exam_taker.py**: This script captures multiple-choice questions for a single course.

2. **multi_exam_taker.py**: This script captures multiple-choice questions for all courses in all tracks, making it the more versatile choice.

To run the multi_exam_taker.py script, use the following command, specifying the number of times you want to run the Python script (`-n`) and the text title of the track to click (`-t`):

```bash
./run_multi_exam_script.sh -n 5 -t "YourTrackText"
```

The `-n` option allows you to control how many times the script runs, while the `-t` option is used to specify the track you want to target. Make sure to replace `"YourTrackText"` with the actual title of the track you wish to automate.

## PNG to PDF Conversion

In this repository, you'll also find a useful script called `png2pdf.py`. This script converts all PNG screenshots captured during the exam-taking process into a single PDF file. Note that scanning the PDF for OCR (Optical Character Recognition) is not within the scope of this script. You can use available tools like PDF24 OCR Creator or similar services to perform OCR on the generated PDF.

Here's how to use `png2pdf.py`:

1. Run the script to convert PNG files to PDF:

    ```bash
    python png2pdf.py
    ```

2. Save the resulting PDF as `output.pdf` in the same directory.

3. Send `output.pdf` to a tool like PDF24 OCR Creator or an OCR service of your choice. This will enable you to obtain an OCR-ed PDF that can be saved in the same directory.

With this improved README, users will have clear instructions on how to set up and utilize the Automate-Percipio project effectively for their automation needs.
