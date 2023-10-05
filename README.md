# Automate-Percipio

**Automate-Percipio** is a set of scripts designed to automate multiple-choice exams on the Percipio platform.

## Setup

1. **Clone and Install**:

    ```bash
    git clone https://github.com/ismailkhan-dev/automate-percipio.git
    pip install -r requirements.txt
    ```

2. **Setup Credentials**:
   In the project root, create `secret.py` with your Percipio login:

    ```python
    USERNAME = "your_username"
    PASSWORD = "your_password"
    ```

    _Reminder_: Add `secret.py` to `.gitignore`.

3. **Give Script Permissions**:
    ```bash
    chmod +x run_multi_exam_script.sh
    ```

## Using the Exam Taker

There are two main scripts:

-   `exam_taker.py` for a single course.
-   `multi_exam_taker.py` for all courses in tracks.

**Example**: To run `multi_exam_taker.py` 5 times targeting "SampleTrack":

```bash
./run_multi_exam_script.sh -n 5 -t "SampleTrack"
```

3. **Execute the Script**:
   Run the script using:

    ```bash
    ./run_multi_exam_script.sh -n [NUMBER_OF_TIMES] -t "[YOUR_TRACK_TEXT]"
    ```

    Where:

    - `[NUMBER_OF_TIMES]` is how often you want the Python script to run.
    - `[YOUR_TRACK_TEXT]` is the title of the track you're targeting.

    For instance, to run it 5 times for "SampleTrack":

    ```bash
    ./run_multi_exam_script.sh -n 5 -t "SampleTrack"
    ```

_Note_: The script temporarily modifies `multi_exam_taker.py` by replacing `PLACEHOLDER` with your track text but reverts back post-execution.

## PNG to PDF

Convert captured PNG screenshots to a single PDF:

```bash
python png2pdf.py
```

For OCR capabilities, use tools like PDF24 OCR Creator on the generated `output.pdf`.
