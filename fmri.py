#!/usr/bin/env python
from nilearn import datasets
from nilearn.input_data import NiftiMasker
import os
import numpy as np
from sklearn.cross_validation import KFold
from nilearn.image import index_img
import sys
import label_prep

subject = sys.argv[0]
label_type = sys.argv[1]
algorithm = sys.argv[2]

files = {}
fmri, labels = label_prep.process_emotion_labels(subject) 
	

root_dir = '.'


 
		
mask = label_prep.get
data = file
labels = ####GETLABELS####
	#Deterimine which data has a label, and which does not
fmri_img = index_img(data, label_type)
		
		#GET IMAGE FROM DATA; Q: n_jobs?
fmri_img = index_img
mask_img = load_img(mask)
process_mask = mask_img.get_data.astype(np.int)
picked_slize = 29
process_mask[..., (picked_slice + 1):] = 0
process_mask[..., :picked_slice] = 0
process_mask [:, 30:] = 0

process_mask_img = new_img_like(mask_img, process_mask)
cv = KFold(y.size, n_folds=4)
searchlight = nlearn.decoding.SearchLight(
	mask_img,
	process_mask_img=process_mask_img,
	radius = 5.0,
	n_jobs = 1,
	verbose=1,
	cv=cv,
	)
searchlight.fit(fmri_img, labels)
			
