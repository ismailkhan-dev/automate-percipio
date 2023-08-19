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


## png2pdf.py

This script will convert all png screenshots into a single pdf file. Scanning the pdf for OCR is out of scope for this script. We can use available tools like PDF24 OCR Creator or something similar. 

Save the pdf as output.pdf to the directory. 

Send output.pdf to PDF24 and use OCR service. It will save ocred pdf to the same directory. 