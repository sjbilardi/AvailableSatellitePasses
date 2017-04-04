# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 19:29:43 2016

@author: Sergei Bilardi

Descrition: Seperate each satellite from csv file

"""

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import tkinter as tk
from tkinter import filedialog

# %% Select STK access reports
# root = tk.Tk()
# root.withdraw()
# file_path = filedialog.askopenfilenames(initialdir="C:\\Users\eagles\Desktop",
#                                         title="Select Access Reports")

# get list of files in directory
cwd = os.getcwd()
file_dir = cwd+"/examplePasses/"
file_path = sorted(os.listdir(file_dir))

# verify files, use only csv
if not file_path:
    print('No file selected.')
    quit()
else:
    fits_extensions = ['.csv', '.CSV']

    file_path = [n for n in file_path if os.path.splitext(n)[1]
                 in fits_extensions]
    file_path = sorted(file_path)

# go through each csv
for file_name in file_path:
	# get name of file
	name = file_name.split('/')[-1].split('.')[0]
	sat_number = 1
	# parse through file
	with open(file_dir+"/"+file_name) as file:
		data = []
		# check each line
		for line in file:
			data.append(line)
			# if line is newline statement only
			if line is '\n':
				if not os.path.exists(file_dir+"/"+name+'/'):
					os.makedirs(file_dir+"/"+name)
				# get pad 0 if single digit 
				if sat_number < 10:
					numb = '0'+str(sat_number)
				else:
					numb = str(sat_number)
				# make new file to save
				sat_file = open(file_dir+"/"+name+'/'+name+'_'+str(numb)
													+'.csv', 'w')
				# write data for each satellite to new file
				for d in data:
					sat_file.write(d)
				# close file and clear "data"
				sat_file.close()
				data = []
				sat_number = sat_number + 1

