# Manage Attendance

This script  automates the attendance keeping of the students by integrating the current attendance records into the main attendance file.

First of all, Python 3.x should be installed in your system.

Also, the package pip should be installed.

Now, in order to install the required packages, you can run the following command:

<b>$ pip install -r requirements.txt</b>

The repository comes with two samples CSV files which contain students' records. <br>
Book1.csv is the main attendance file <br>
Book2.csv is the current attendance file

In order to automate the integration, run the following command where we are passing several commandline arguments

<b>$ python transfer.py Book1.csv Book2.csv name name "Sep 2"</b>

where,
Book1.csv is the main attendance file <br>
Book2.csv is the current attendance file <br>
name is the column name of students_name in the main attendance file <br>
name is the column name of students_name in the current attendance file <br>
"Sep 2" is the column name that is going to be added in the main attendance file. This should be changed accordingly.
