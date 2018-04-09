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

subject = sys.argv[1]
label_type = sys.argv[2]
#algorithm = sys.argv[3]

files = {}
avg_fmri, labels = label_prep.get_img_labels(subject) 
bg_img = image.mean_img(avg_fmri)
	

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


label_mask = np.logical_not(label_col.isin( ['.'] )).values.ravel()
clean_labels = label_col[label_mask].values.ravel()
#print(clean_labels.shape)

#Process fMRI
#Get Mask
from nilearn.input_data import NiftiMasker
masker = NiftiMasker(mask_strategy='epi', standardize=True)
fmri_masked = masker.fit_transform(avg_fmri)
#print(fmri_masked.shape)
print('Training on {} episodes using {} features'.format(label_mask.shape[0], \
        fmri_masked.shape[1]))

#filter by label
fmri_masked = fmri_masked[label_mask]
 

#SVC stuff
from sklearn.svm import SVC
svc = SVC(kernel='linear')
session_label = labels['run'][label_mask].values.ravel()

#file prefix
prefix = 'output/simple_svc_{}_{}'.format(subject, label_type)

if False:
    from sklearn.cross_validation import LeaveOneLabelOut, cross_val_score
    cv = LeaveOneLabelOut(session_label)
    cv_score = cross_val_score(svc, fmri_masked, clean_labels, cv=cv, n_jobs=8)
    print("Results for subject {}:".format(subject))
    print(cv_score)
    # write scores to log file
    with open('output/log.txt', 'a') as fh:
        log_line = ['SVC', subject, label_type]
        log_line.extend(cv_score)
        log_line = [str(x) for x in log_line]
        fh.write('\t'.join(log_line) + '\n')

svc.fit(fmri_masked, clean_labels)

training_score = svc.score(fmri_masked, clean_labels)
print("Score for training data = {}".format(training_score))

coef = svc.coef_
coef_img = masker.inverse_transform(coef)
coef_img.to_filename(prefix + '_tmap.nii')

# plot
plot_stat_map(coef_img, bg_img=bg_img, title='Subject {}, {}'.format(subject, label_type))\
        .savefig(prefix + '_weights.svg')

# broken pickle saving?
with open(prefix + '.svc', 'wb') as fh:
    pickle.dump(svc, fh, pickle.HIGHEST_PROTOCOL)
