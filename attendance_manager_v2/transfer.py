import pandas as pd
import numpy as np
import sys

import re

import nltk
nltk.download('stopwords')
#nltk.download('words')
from nltk.corpus import stopwords
nltk_stop_words = set(stopwords.words('english'))

# Format of the command:
# python python_file_name.py MODE MainCSVFileName.csv CurrentCSVFileName.csv MAIN_FILE_COL_NAME CURRENT_FILE_COL_NAME NEW_ADDED_COL_NAME

# If Mode is 1, the format of the command is
# python python_file_name.py MODE MainCSVFileName.csv CurrentCSVFileName.csv MAIN_FILE_COL_NAME CURRENT_FILE_COL_NAME NEW_ADDED_COL_NAME

# If Mode is 0, the format of the command is
# python python_file_name.py MODE MAINCSVFileName.csv MAIN_FILE_COL_NAME FILE1.{JPG|PNG} FILE2.{JPG|PNG} ...  NEW_ADDED_COL_NAME


'''
This script automates the attendance keeping of the students by integrating the current attendance records into the main attendance file.

Created on: 27 August 2020
Created by: Ranjan Shrestha, ranjan.shrestha.np@gmail.com

Program bugs should be directed to ranjan(dot)shrestha(dot)np(at)gmail(dot)com

'''

__author__ = 'ranjan-stha'

# Cleans the string by stripping and removing trailing spaces
def clean_string(x):
	x.strip()
	x.replace(" ", "")
	#print (x)
	x = re.sub(r"[^a-zA-Z ]+", '', x)#re.sub(r'\d*', '', x)

	#x = [x for x.split()
	#print (x)
	return " ".join([x for x in x.split() if len(x)>2]) # for name or surname the length is most probably more than 2 letters

def filter_nltk_stop_words(x):
	return ' '.join(list(set(x.split()) - nltk_stop_words))

# Search in the substring for a match
def search_string_1(x):
	for current_name in current_names:
		if current_name.split()[0] in x and current_name.split()[-1] in x:
			return True
	return False

# Search in the substring for a match
def search_string_2(x):
	for current_name in current_names:
		if x.split()[0] in current_name and x.split()[-1] in current_name:
			return True

	return False

# Resizes the image
def resize_image(img, scale_factor):
	return cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation = cv2.INTER_CUBIC)

# Sharpen the image for better detection
def sharpen_image(img):
	kernel = np.array([[-1,-1,-1], 
                   [-1, 9,-1],
                   [-1,-1,-1]])

	return cv2.filter2D(img, -1, kernel)

TESSERACT_PATH = 'C:/Tesseract-OCR/tesseract'

print (f"Number of arguments: {len(sys.argv)}")
print (f"Argument list: {str(sys.argv)}")

MODE = int(sys.argv[1])

# Initialization
MAIN_FILE = None
CURRENT_FILE = None
MAIN_COL_NAME = None
CURRENT_COL_NAME = None
NEW_COL = None

if MODE == 1: # takes in csv file
	if len(sys.argv) != 7:
		print ("Five arguments should be present")
		print ("Exiting!!")
		sys.exit(0)

	MAIN_FILE = sys.argv[2]
	CURRENT_FILE = sys.argv[3]
	MAIN_COL_NAME = sys.argv[4]
	CURRENT_COL_NAME = sys.argv[5]
	NEW_COL = sys.argv[6]

elif MODE == 0: # takes in jpg/png images
	try:
		MAIN_FILE = sys.argv[2]
		MAIN_COL_NAME = sys.argv[3]
		CURRENT_FILE = sys.argv[4:-1]
		NEW_COL = sys.argv[-1]

		import pytesseract
		import cv2

		pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
	except Exception as e:
		print (e)
		print ("It seems you have not provided enough arguments")
		print ("Exiting")
		sys.exit(0)

# Reading data frames 
df_main = pd.read_csv(MAIN_FILE, sep=';|,', engine='python')

if MODE == 1:
	df_current = pd.read_csv(CURRENT_FILE, sep=';|,', engine='python')
	current_names = df_current[CURRENT_COL_NAME].str.lower().map(clean_string).values
elif MODE == 0:
	current_names = []
	current_file_list = CURRENT_FILE
	for file in current_file_list:
		img_cv = cv2.imread(file)
		
		if img_cv is None:
			print ("Error: Image could not be read. Check the filename (and extension)")
			print ("Exiting !!")
			sys.exit(0)

		img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

		adaptive_threshold = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)
		resized_img = resize_image(adaptive_threshold, 1.5)

		sharpened_img = sharpen_image(resized_img)

		config = "--psm 3"
		splitted_text = list(pd.Series(pytesseract.image_to_string(sharpened_img, config=config).lower().split('\n')).map(clean_string))
		
		splitted_text = [filter_nltk_stop_words(x) for x in splitted_text]
		
		splitted_text = [x for x in splitted_text if x and len(x)<25 and len(x)>5]
		current_names.append(splitted_text)

	current_names = list(set([item for sublist in current_names for item in sublist]))  # flatteing the list
	print ('='*50)
	print (f"The list of names extracted from images are \n {current_names}")

# Processed the data
if MODE == 1:
	processed_current_data_1 = list(df_main[MAIN_COL_NAME].str.lower().map(clean_string).map(search_string_1))
	processed_current_data_2 =  list(df_main[MAIN_COL_NAME].str.lower().map(clean_string).isin(df_current[CURRENT_COL_NAME].str.lower().map(clean_string)).values)
elif MODE == 0:
	processed_current_data_1 = list(df_main[MAIN_COL_NAME].str.lower().map(clean_string).map(search_string_2))
	processed_current_data_2 = list(df_main[MAIN_COL_NAME].str.lower().map(clean_string).isin(pd.Series(current_names).str.lower()).values)

final_processed_data = processed_current_data_1 or processed_current_data_2

# Add a new column to the main dataframe
df_main[NEW_COL] = ['P' if x else 'A' for x in final_processed_data]

print ('='*50)
# Displaying the final result in main dataframe (MAX=100 records)
print (df_main.head(100))

# Store the dataframe to the main csv file
df_main.to_csv(MAIN_FILE, index=False, header=True, sep=',')