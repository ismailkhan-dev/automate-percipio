# automate-percipio

This project takes multiple choice exams on the percipio platform. It uses Python and Selenium. 

Main purpose of this project serves as a web automation bot. 

## Running the exam taker script

There are two exam taker scripts: 
1. exam_taker.py
2. multi_exam_taker.py

exam_taker.py will screen cap multiple choice questions of a single course.
multi_exam_taker.py will screen cap multiple choice questions of all courses in all tracks. 

Obviously, multi_exam_taker.py is the more useful script. 


## img2pdf.py

This script will convert all png files in a folder and output a pdf file that is scanned with OCR. The user can search for answers when answering the exam for a pass. 
