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
import ml_prep

subject = sys.argv[1]
label_type = sys.argv[2]
percentile = float(sys.argv[3])

print("Running reduced SVC learning on subject {} for label type {} and keeping {}% of voxels."
        .format(subject, label_type, percentile))

avg_fmri, labels = label_prep.get_img_labels(subject) 
bg_img = image.mean_img(avg_fmri)
	
fmri_masked, masker, labels, runs = ml_prep.get_fmri_masker_labels_runs(subject, label_type)

#SVC stuff
from sklearn.svm import SVC
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.pipeline import Pipeline
feature_selection = SelectPercentile(f_classif, percentile=percentile)
svc = SVC(kernel='linear')
anova_svc = Pipeline([('anova', feature_selection), ('svc', svc)])

#file prefix
prefix = 'output/reduced_svc_{}_{}_{}'.format(subject, label_type, percentile)

if True:
    from sklearn.cross_validation import LeaveOneLabelOut, cross_val_score
    cv = LeaveOneLabelOut(runs)
    cv_score = cross_val_score(anova_svc, fmri_masked, labels, cv=cv, n_jobs=8)
    print("Results for subject {}:".format(subject))
    print(cv_score)
    # write scores to log file
    with open('output/log_svc_reduced.txt', 'a') as fh:
        log_line = ['Anova-SVC', subject, label_type, percentile]
        cv_score = np.mean(cv_score)
        cv_score = "{0:.2f}".format(cv_score)
        log_line.append(cv_score)
        log_line = [str(x) for x in log_line]
        fh.write('\t'.join(log_line) + '\n')

anova_svc.fit(fmri_masked, labels)

training_score = anova_svc.score(fmri_masked, labels)
print("Score for training data = {}".format(training_score))

coef = svc.coef_
coef = feature_selection.inverse_transform(coef)
coef_img = masker.inverse_transform(coef)
coef_img.to_filename(prefix + '_tmap.nii')

# plot
plot_stat_map(coef_img, bg_img=bg_img, title='Subject {}, {}'.format(subject, label_type))\
        .savefig(prefix + '_weights.svg')

# broken pickle saving?
with open(prefix + '.anova-svc', 'wb') as fh:
    pickle.dump(anova_svc, fh, pickle.HIGHEST_PROTOCOL)
