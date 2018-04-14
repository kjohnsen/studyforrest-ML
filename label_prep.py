#!/usr/env/python3

import pandas as pd
from nilearn.image import concat_imgs, index_img, mean_img, load_img
from math import ceil
import pickle
import os.path


def get_session_info(start, end, hrfOffset):
    if hrfOffset:
        start += 2
        end += 4
    if start >= 6410:
        session = 8
        offset = 6410
    elif start >= 5342:
        session = 7
        offset = 5342
    elif start >= 4480:
        session = 6
        offset = 4480
    elif start >= 3572:
        session = 5
        offset = 3572
    elif start >= 2612:
        session = 4
        offset = 2612
    elif start >= 1752:
        session = 3
        offset = 1752
    elif start >= 886:
        session = 2
        offset = 886
    else:
        session = 1
        offset = 0

    start_frame = ceil((start - offset) / 2)
    end_frame = ceil((end - offset) / 2)

    return session, start_frame, end_frame

def get_nii_filename(run, subject):
    #Remember subject must have 0 before it if in single digits
    path = 'sub-{}/run{}/sub-{}_ses-movie_task-movie_run-{}_bold.nii'\
            .format(subject, run, subject, run)
    return path


def get_mask_filename(run, subject):
    #Remember subject must have 0 before it if in single digits
    path = 'sub-{}/run{}/sub-{}_ses-movie_task-movie_run-{}_defacemask.nii'\
            .format(subject, run, subject, run)
    return path

def process_emotion_labels(subject, label_file, offset=False):

    data_filename = "labels/segmentation/emotions_av_1s_thr50.tsv"
    #labels = pd.read_csv(data_filename, sep='\t')
    #return labels

    rows = []
    # start with first session loaded
    prev_run = 1
    run_img = load_img(get_nii_filename(prev_run, subject))
    result_imgs = []
    # iterate over labels
    with open(data_filename, 'r') as fh:
        counter = 0
        for line in fh:
            counter += 1
            #if counter > 10: break
            # build dataframe row
            line = line.strip().split('\t')
            start, end = line[:2]
            start = float(start)
            end = float(end)
            char, tags, arousal, val_pos, val_neg = [x.split('=')[1] for x in line[2].split(' ')]
            #TODO: get char arousal direction emotion
            tags = tags.split(',')
            if 'ha' in tags:
                arousal = 'high'
            elif 'la' in tags:
                arousal = 'low'
            else:
                arousal = '.'

            if float(val_pos) > 0:
                valence = 'pos'
                if float(val_neg) > 0:
                    valence = 'both'
            elif float(val_neg) > 0:
                valence = 'neg'
            else: valence = '.'


            if 'self' in tags:
                direction = 'self'
            elif 'other' in tags:
                direction = 'other'
            else:
                direction = '.'

            
            # get run, start, end
            run, start_frame, end_frame = get_session_info(start, end, offset)
            # get NiImg object and append to results
            if run != prev_run:
                prev_run = run
                run_img = load_img(get_nii_filename(prev_run, subject))
            episode_img = index_img(run_img, range(start_frame, end_frame+1))
            episode_img = mean_img(episode_img)
            assert len(episode_img.shape) == 3 # make sure it's 3D
            result_imgs.append(episode_img)

            rows.append([char, arousal, valence, direction, run])

    result_imgs = concat_imgs(result_imgs, auto_resample=True)
    label_df = pd.DataFrame(rows, columns=['char', 'arousal', 'valence', 'direction', 'run'])

    label_df.to_csv(label_file, index=False)
    with open(get_img_filename(subject), 'wb') as fh:
        pickle.dump(result_imgs, fh, pickle.HIGHEST_PROTOCOL)

def get_img_filename(subject):
    return 'cache/episode_means_sub-{}_Nifti1Image.pkl'.format(subject)


def get_img_labels(subject, offset=False):
    img_file = get_img_filename(subject)
    offset_string = '_offset' if offset else ''
    label_file = 'cache/label_df{}.csv'.format(offset_string)
    if not os.path.isfile(label_file) or not os.path.isfile(img_file):
        process_emotion_labels(subject, label_file, offset)
    labels = pd.read_csv(label_file)
    with open(img_file, 'rb') as fh:
        imgs = pickle.load(fh)
    return imgs, labels



if __name__ == "__main__":
    for sub in ['01', '02', '03', '04', '05']:
        label_file = 'cache/label_df_offset.csv'
        offset=True
        process_emotion_labels(sub, label_file, offset)
