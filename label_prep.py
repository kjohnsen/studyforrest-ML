#!/usr/env/python3

import pandas as pd
from nilearn.image import concat_imgs, index_img, mean_img, load_img
from math import ceil

def get_session_info(start, end):
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

def process_emotion_labels(subject):

    data_filename = "labels/segmentation/emotions_av_1s_thr50.tsv"
    #labels = pd.read_csv(data_filename, sep='\t')
    #return labels

    rows = []
    # start with first session loaded
    prev_session = 1
    session_img = load_img(get_nii_filename(prev_session, subject))
    result_imgs = []
    # iterate over labels
    counter = 0
    with open(data_filename, 'r') as fh:
        for line in fh:
            print(line)
            counter += 1
            if counter > 10: break
            # build dataframe row
            line = line.strip().split('\t')
            start, end = line[:2]
            start = float(start)
            end = float(end)
            char, tags, arousal, val_pos, val_neg = [x.split('=')[1] for x in line[2].split(' ')]
            rows.append([start, end, char, arousal, val_pos, val_neg])
            
            # get session, start, end
            session, start_frame, end_frame = get_session_info(start, end)
            # get NiImg object and append to results
            if session != prev_session:
                prev_session = session
                session_img = load_img(get_nii_filename(prev_session, subject))
            episode_img = index_img(session_img, range(start_frame, end_frame+1))
            episode_img = mean_img(episode_img)
            assert len(episode_img.shape) == 3 # make sure it's 3D
            result_imgs.append(episode_img)

    result_imgs = concat_imgs(result_imgs)
    label_df = pd.DataFrame(rows, columns=['start', 'end', 'char', 'arousal', 'val_pos', 'val_neg'])

    return result_imgs, label_df


if __name__ == "__main__":
    img, labels = process_emotion_labels('01')
    print(labels)
