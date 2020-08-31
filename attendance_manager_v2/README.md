# Manage Attendance using Optical Character Recognition(OCR)

This script  automates the attendance keeping of the students by integrating the current attendance records into the main attendance file.

First of all, Python 3.x should be installed in your system.

Also, the package pip should be installed.

Now, in order to install the required packages, you can run the following command:

<b>$ pip install -r requirements.txt</b>

The repository comes with two samples CSV files which contain students' records. <br>
Book1.csv is the main attendance file <br>
Book2.csv is the current attendance file

With this script, you can either use images or csv file to integrate the attendance.

To use Images, just take the snapshot of the screen of the attendance of the students, then run the script as follows:

Before you run the script, you need to install pytesseract.

For Windows machine, find the executable file in this link: https://github.com/UB-Mannheim/tesseract/wiki

Install this executable in drive C:\

After the installation, you can run the below script.

<b>$ python 0 transfer.py Book1.csv name <image1.{jpg|png} image2.{jpg|png} ......> "Sep 2" </b> </br>

<i> Note: You can pass as many image files as you want </i>

The alternative is to use the current attendance list in csv format. Run the script as follows:

<b>$ python 1 transfer.py Book1.csv Book2.csv name name "Sep 2"</b>

where,
Book1.csv is the main attendance file <br>
Book2.csv is the current attendance file <br>
name is the column name of students_name in the main attendance file <br>
name is the column name of students_name in the current attendance file <br>
"Sep 2" is the column name that is going to be added in the main attendance file. This should be changed accordingly.
