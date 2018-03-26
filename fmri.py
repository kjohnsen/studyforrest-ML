#!/usr/bin/env python
from nilearn import datasets
from nilearn.input_data import NiftiMasker
import os


root_dir = '.'

for subdiirs, dirs, files in os.walk(root_dir):
	mask = None
	data = None
	for file in files: 
		if "defacemask" in file
			print("Mask" + file)
			mask = file
