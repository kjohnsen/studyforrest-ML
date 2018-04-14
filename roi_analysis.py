from nilearn import plotting
from nilearn.regions import signals_to_img_labels
import ml_prep
import numpy as np

subject = '01'
label_type = 'arousal'


### SVM on Cortical ==============================
fmri_masked, masker, clean_labels, session_label = ml_prep.get_fmri_masker_labels_runs(\
        subject, label_type, 'cort')
from sklearn.svm import SVC
svc = SVC(kernel='linear')

#file prefix
prefix = 'output/cort_roi_svc_{}_{}'.format(subject, label_type)

if True:
    from sklearn.cross_validation import LeaveOneLabelOut, cross_val_score
    cv = LeaveOneLabelOut(session_label)
    cv_score = cross_val_score(svc, fmri_masked, clean_labels, cv=cv, n_jobs=8)
    score = np.mean(cv_score)
    print("Accuracy for cortical ROIs on subject {}: {}".format(subject, score))

svc.fit(fmri_masked, clean_labels)

coef = svc.coef_
##print("2D array shape", fmri_masked.shape)
#print("coef shape", coef.shape)
#atlas = ml_prep.get_atlas_img_labels('cort')[0]
#print("atlas shape", atlas.shape)
#coef_img = signals_to_img_labels(coef, atlas)
#print("coef_img shape", coef_img.shape)
##coef_img = masker.inverse_transform(coef)
#coef_img.to_filename(prefix + '_tmap.nii')

print("SVM weights for cortical regions:")
print("Temporal fusiform cortex, anterior division: {0:.2f}".format(coef[0, 36]))
print("Temporal fusiform cortex, posterior division: {0:.2f}".format(coef[0, 37]))
mean_cort = np.mean(coef)
print("Mean for all cortical regions: {0:.2f}".format(mean_cort))

# plot
#plotting.plot_glass_brain(coef_img, title='Subject {}, {}'.format(subject, label_type))\
#        .savefig(prefix + '_glass.svg')


### SVM on Subcortical ================================
fmri_masked, masker, clean_labels, session_label = ml_prep.get_fmri_masker_labels_runs(\
        subject, label_type, 'sub')
svc = SVC(kernel='linear')

#file prefix
prefix = 'output/sub_roi_svc_{}_{}'.format(subject, label_type)

if True:
    cv = LeaveOneLabelOut(session_label)
    cv_score = cross_val_score(svc, fmri_masked, clean_labels, cv=cv, n_jobs=8)
    score = np.mean(cv_score)
    print("Accuracy for subcortical ROIs on subject {}: {}".format(subject, score))

svc.fit(fmri_masked, clean_labels)

coef = svc.coef_
#coef_img = masker.inverse_transform(coef)
#coef_img.to_filename(prefix + '_tmap.nii')
# weights
print("SVM weights for subcortical regions:")
print("Left amygdala: {0:.2f}".format(coef[0, 9]))
print("Right amygdala: {0:.2f}".format(coef[0, 19]))
mean_sub = np.mean(coef)
print("Mean for all subcortical regions: {0:.2f}".format(mean_sub))
# plot
#plotting.plot_glass_brain(coef_img, title='Subject {}, {}'.format(subject, label_type))\
#        .savefig(prefix + '_glass.svg')
