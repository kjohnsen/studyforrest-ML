#!/usr/bin/env python
from copy import deepcopy
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
import ml_prep

subject = sys.argv[1]
label_type = sys.argv[2]

if sys.argv[3] == 'True':
    offset = True
else:
    offset = False

avg_fmri, labels = label_prep.get_img_labels(subject, offset) 
bg_img = image.mean_img(avg_fmri)
	
fmri_masked, masker, clean_labels, session_label = \
        ml_prep.get_fmri_masker_labels_runs(subject, label_type, offset=offset)

#SVC stuff
from sklearn.svm import SVC
svc = SVC(kernel='linear')

#file prefix
prefix = 'output/simple_svc_{}_{}'.format(subject, label_type)

if True:
    from sklearn.cross_validation import LeaveOneLabelOut, cross_val_score
    cv = LeaveOneLabelOut(session_label)
    cv_score = cross_val_score(svc, fmri_masked, clean_labels, cv=cv, n_jobs=8)
    print("Results for subject {}:".format(subject))
    print(cv_score)
    # write scores to log file
    with open('output/log.txt', 'a') as fh:
        log_line = ['SVC', subject, label_type]
        alt_log_line = deepcopy(log_line)
        alt_log_line.extend(cv_score)
        cv_score = np.mean(cv_score)
        cv_score = "{0:.2f}".format(cv_score)
        log_line.append(cv_score)
        if offset: log_line.append("offset")
        else: log_line.append("no_offset")
        log_line = [str(x) for x in log_line]
        log_line = '\t'.join(log_line)
        alt_log_line = [str(x) for x in alt_log_line]
        alt_log_line = '\t'.join(alt_log_line)
        fh.write(log_line + '\n')
        #print(log_line)
        print(alt_log_line)

#svc.fit(fmri_masked, clean_labels)

#training_score = svc.score(fmri_masked, clean_labels)
#print("Score for training data = {}".format(training_score))

#print('fmri_masked shape', fmri_masked.shape)
#coef = svc.coef_
#print('coef shape', coef.shape)
#coef_img = masker.inverse_transform(coef)
#print('coef_img shape', coef_img.shape)
#coef_img.to_filename(prefix + '_tmap.nii')
#
## plot
#plot_stat_map(coef_img, bg_img=bg_img, title='Subject {}, {}'.format(subject, label_type))\
#        .savefig(prefix + '_weights.svg')
#
## broken pickle saving?
#with open(prefix + '.svc', 'wb') as fh:
#    pickle.dump(svc, fh, pickle.HIGHEST_PROTOCOL)
