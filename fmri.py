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
from nilearn.plotting import plot_stat_map, plot_img, show
from nilearn import image
import pickle
from nilearn import decoding

subject = sys.argv[1]
label_type = sys.argv[2]
algorithm = sys.argv[3]

files = {}
avg_fmri, labels = label_prep.get_img_labels(subject) 
print("avg_fmri")
print(avg_fmri.shape)
print("labels")
print(labels.shape)	
print(labels)

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


label_mask = ~label_col.isin( ["."] )

label_mask = label_mask.values.ravel()
clean_labels = label_col[label_mask]
clean_labels = clean_labels.values.ravel()
#Process fMRI
clean_fmri_img = index_img(avg_fmri, label_mask)

smooth_img = image.smooth_img(clean_fmri_img,  fwhm='fast')

#Get Mask
mask_file = label_prep.get_mask_filename(1, subject) 
mask_img = image.load_img(mask_file)

#Get Process Mask
process_mask = mask_img.get_data().astype(np.int)
picked_slice = 29
process_mask[..., (picked_slice + 1):] = 0
process_mask[..., :picked_slice] = 0
process_mask [:, 30:] = 0
process_mask_img = image.new_img_like(mask_img, process_mask)

#CrossValidation
cv = KFold(clean_labels.size, n_folds=4)

searchlight = decoding.SearchLight(
	mask_img,
	process_mask_img=process_mask_img,
	radius = 5.0,
	estimator=algorithm,
	n_jobs = 1,
	verbose=1,
	cv=cv,
	)

searchlight.fit(smooth_img, clean_labels)

#Get searchlight_img, and plot it
mean_fmri = image.mean_img(smooth_img)
searchlight_img = image.new_img_like(mean_fmri, searchlight.scores_)

sl_path = algorithm + "_" + "sub" + subject + "_searchlight_plot.svg"


filename = algorithm + "_" + subject + "_scorespyobj"
with open(filename, 'wb') as file:
        pickle.dump(searchlight.scores_, file, pickle.HIGHEST_PROTOCOL)
	
searchlight_plot =plot_img(searchlight_img, bg_img=mean_fmri,
         title="Searchlight", display_mode="z", cut_coords=[-9], output_file=sl_path,
         vmin=.42, cmap='hot', threshold=.2, black_bg=True)


filename = algorithm + "_" + subject + "_searchlightmap_pyobj"  
with open(filename, 'wb') as file:
        pickle.dump(searchlight_plot, file, pickle.HIGHEST_PROTOCOL)

#fScore_img,plotted
p_ma = np.ma.array(p_unmasked, mask=np.logical_not(process_mask))
f_score_img = new_img_like(mean_fmri, p_ma)

stat_path = algorithm + "_" + "sub" + subject + "_statmap_plot.svg"
statmap = plot_stat_map(f_score_img, mean_fmri,
              title="F-scores", display_mode="z",
              cut_coords=[-9], output_file=stat_path,
              colorbar=False)

filename = algorithm + "_" + subject + "_statmap_pyobj" 
with open(filename, 'wb') as file:
        pickle.dump(statmap, file, pickle.HIGHEST_PROTOCOL)

		
