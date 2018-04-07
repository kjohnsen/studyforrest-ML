#!/usr/bin/env python
from nilearn import datasets
from nilearn.input_data import NiftiMasker
import os
import numpy as np
from sklearn.cross_validation import KFold
from nilearn.image import index_img
import sys
import label_prep
import math
subject = sys.argv[0]
label_type = sys.argv[1]
algorithm = sys.argv[2]

files = {}
avg_fmri, labels = label_prep.get_emotion_labels(subject) 
	

#PROCESS LABELS
if label_type == "valence":
	label_col = labels[['valence' ]]
elif label_type == "arousal":
	label_col = labels[['arousal' ]]

elif label_type == "direction":
        label_col = labels[['direction' ]]

elif label_type == "emotion":
        label_col = labels[['emotion']]

else:
	print("Check label type")
	exit(0)
label_mask = ~labels.isin( {math.inf} )
clean_labels = label_col[label_mask]
#Process fMRI
clean_fmri_img = index_img(avg_fmri, label_mask)
smooth_img = image.smooth_img(clean_fmri_img)
 
#Get Mask
mask_file = label_prep.get_mask_filename(0, subject) 
mask_img = load_img(mask_file)

#Get Process Mask
process_mask = mask_img.get_data.astype(np.int)
picked_slize = 29
process_mask[..., (picked_slice + 1):] = 0
process_mask[..., :picked_slice] = 0
process_mask [:, 30:] = 0
process_mask_img = new_img_like(mask_img, process_mask)

#CrossValidation
cv = KFold(clean_labels.size, n_folds=4)

searchlight = nlearn.decoding.SearchLight(
	mask_img,
	process_mask_img=process_mask_img,
	radius = 5.0,
	estimator=algorithm
	n_jobs = 1,
	verbose=1,
	cv=cv,
	)
searchlight.fit(smooth_img, clean_labels)


from nilearn import image
mean_fmri = image.mean_img(fmri_img)

from nilearn.plotting import plot_stat_map, plot_img, show
searchlight_img = new_img_like(mean_fmri, searchlight.scores_)			
