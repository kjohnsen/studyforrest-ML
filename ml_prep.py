import label_prep
from nilearn.image import mean_img
import numpy as np
import sys

def get_fmri_masker_labels_runs(subject, label_type):
    subject = sys.argv[1]
    label_type = sys.argv[2]

    avg_fmri, labels = label_prep.get_img_labels(subject) 
    avg_fmri = image.smooth_img(avg_fmri, fwhm='fast')
    bg_img = mean_img(avg_fmri)
            

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

    from nilearn.input_data import NiftiMasker
    masker = NiftiMasker(mask_strategy='epi', smoothing_fwhm=4, standardize=True)
    fmri_masked = masker.fit_transform(avg_fmri)
    fmri_masked = fmri_masked[label_mask]
    #print(fmri_masked.shape)
    print('Prepped data for {} episodes and {} features'.format(label_mask.shape[0], \
            fmri_masked.shape[1]))

    runs = labels['run'][label_mask].values.ravel()

    return fmri_masked, masker, clean_labels, runs
