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
from nilearn.input_data import NiftiMasker
from sklearn.feature_selection import f_classif
import warnings

#warnings.simplefilter('error', UserWarning)
subject = sys.argv[1]
label_type = sys.argv[2]
algorithm = sys.argv[3]

files = {}
avg_fmri, labels = label_prep.get_img_labels(subject) 


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
nifti_masker = NiftiMasker( standardize=True, mask_strategy="epi" )
masked_img = nifti_masker.fit_transform(smooth_img)

#mask_file = label_prep.get_mask_filename(1, subject) 
#mask_img = image.load_img(mask_file)

#Get Process Mask
process_mask = nifti_masker.mask_img_.get_data().astype(np.int)
picked_slice = 29
process_mask[..., (picked_slice + 1):] = 0
process_mask[..., :picked_slice] = 0
process_mask [:, 30:] = 0
process_mask_img = image.new_img_like(nifti_masker.mask_img_, process_mask)

#CrossValidation
cv = KFold(clean_labels.size, n_folds=6)
print("presearch")
#Process mask
searchlight = decoding.SearchLight(
	nifti_masker.mask_img_,
	radius = 5.0,
	estimator=algorithm,
	n_jobs = 1,
	verbose=1,
	cv=cv,
	)
print("postsearch")

print(smooth_img.shape)
searchlight.fit(smooth_img, clean_labels)
print(searchlight.scores_.shape)

unique, counts = np.unique(searchlight.scores_, return_counts=True)
map = dict(zip(unique,counts))
print(map) 
#Get searchlight_img, and plot it
mean_fmri = image.mean_img(smooth_img)
searchlight_img = image.new_img_like(mean_fmri, searchlight.scores_)

sl_path = algorithm + "_" + "sub" + subject + "_searchlight_plot.svg"


filename = algorithm + "_" + subject + "_scorespyobj"
#with open(filename, 'wb') as file:
#        pickle.dump(searchlight.scores_, file, pickle.HIGHEST_PROTOCOL)
	
searchlight_plot =plot_img(searchlight_img, bg_img=mean_fmri,
         title="Searchlight", display_mode="z", cut_coords=[-9], output_file=sl_path,
         threshold= 0.1, cmap='hot', black_bg=True)


filename = algorithm + "_" + subject + "_searchlightmap_pyobj"  
#with open(filename, 'wb') as file:
#        pickle.dump(searchlight_plot, file, pickle.HIGHEST_PROTOCOL)

#fScore_img,plotted
		
from sklearn.feature_selection import f_classif
f_values, p_values = f_classif(masked_img, clean_labels)
p_values = -np.log10(p_values)
p_values[p_values > 10] = 10
p_unmasked = nifti_masker.inverse_transform(p_values).get_data()
p_ma = np.ma.array(p_unmasked, mask=np.logical_not(process_mask))
f_score_img = image.new_img_like(mean_fmri, p_ma)

stat_path = algorithm + "_" + "sub" + subject + "_statmap_plot.svg"
statmap = plot_stat_map(f_score_img, mean_fmri,
              title="F-scores", display_mode="z",
              cut_coords=[-9], output_file=stat_path,
              colorbar=False)

filename = algorithm + "_" + subject + "_statmap_pyobj" 
#with open(filename, 'wb') as file:
#        pickle.dump(statmap, file, pickle.HIGHEST_PROTOCOL)

		
