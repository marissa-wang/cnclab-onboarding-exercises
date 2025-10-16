#!/usr/bin/env python

import numpy as np
import pandas as pd
import scipy.io as sio
import scipy.stats as stats
import matplotlib.pyplot as plt
# TIL "seaborn" is from "samuel norman seaborn" => imported as sns
import seaborn as sns

# "grating2AFC S11" probably stands for:
#
# grating -- the sinusoidal visual grating of the experiment
# 2AFC -- 2-alternative forced choice (task); subject is forced to pick between two
# S11 -- Subject 11. they ran this on multiple subjects for sure, and this is only one


### ==================== STEP 1: EXTRACT DATA ==================== ###

def load_data(filename):
    # grating2AFC S11.mat has the data we need in it! But it is binary/archive
    # format, so not directly viewable. Scipy to the rescue :3

    # Transfer data from .mat to variable w/ scipy.io
    grating_all_mat_data = sio.loadmat(filename)

    #print(grating_all_mat_data)
    # The above print statement was used temporarily to set a breakpoint and
    # extrapolate more about what data structure grating_all_mat_data has.
    # Debug mode tells us 'data' = {ndarray: (1,1)}, so we will break this up more.

    # We use grating_all_mat_data['data'] and not grating_all_mat_data[0] since
    # grating_all_mat_data is a dictionary. We extract only the "data" key/category
    # since that is the one of interest.
    grating_all_data = grating_all_mat_data['data']

    # Same concept with extracting specific categories using keys from the
    # dictionary of "data."
    # [0][0][0] at the end is to extract the data from matlab 1x1 structs :(
    #### stim_id -- was grating right or left? (0 = left, 1 = right)
    stim_id = grating_all_data['stimID'][0][0][0]
    #### response -- subject chose which side they thought had grating
    #### (same codes as above)
    response = grating_all_data['response'][0][0][0]
    #### rating -- confidence rating, from 1 (least confident) to 4 (most)
    #### negative value means did not respond in time
    rating = grating_all_data['rating'][0][0][0]
    #### response_rt -- reaction time, between stimulus onset and subject response
    response_rt = grating_all_data['responseRT'][0][0][0]

    # We organize all of this info into a pandas dataframe!
    # Note: pandas.DataFrame expects a dict-like structure;
    # wrapping columns in {} is required to build it correctly.
    grating_df = pd.DataFrame(
        {
            "stimID": stim_id,
            "response": response,
            "rating": rating,
            "responseRT": response_rt,
        }
    )

    # returns final dataframe :3
    return grating_df

### ==================== STEP 2: ANALYZE DATA ==================== ###

## 1.1

def task_1_1(data, first_half_n_trials):

    # Splitting data into first/second halves
    # Add "whichHalf" column with "1-500" or "501-1000" as values
    data['whichHalf'] = np.where(
        data.index < first_half_n_trials, # condition
        "1-500",   # value if T
        "501-1000" # value if F
    )

    # plot them!
    # (does catplot stand for category plot??)
    plot = sns.catplot(
        data = data, # cursed.
        x = "whichHalf",
        y = "responseRT",
        kind = "bar",
        errorbar = "se",
        color = "0.6"
    )

    # The fact I ended up having to import matplotlib for this in the end is... sad
    # (for some reason I thought I could get away with just importing seaborn :'))
    plt.title("Reaction Times: First vs Second Half")
    plt.xlabel("Trial Halves")
    plt.ylabel("Mean Reaction Time (s)")
    plt.tight_layout()
    plt.show()

## 1.2

def task_1_2(data, total_n_trials, first_half_n_trials):

    # Slice the "responseRT" series into two halves
    first_half_RTs = data["responseRT"].iloc[:first_half_n_trials]
    second_half_RTs = data["responseRT"].iloc[first_half_n_trials:total_n_trials]

    # run actual t-test
    result = stats.ttest_ind(
        first_half_RTs,
        second_half_RTs,
    )

    return result.pvalue

## 1.3

def task_1_3(filtered_trials_data):
    # plot median RT for confidence levels 1-4
    plot = sns.catplot(
        data = filtered_trials_data,
        x = "rating",
        y = "responseRT",
        kind = "bar",
        estimator = np.median,
        errorbar = None, # set equal to ("pi", 50) for error bar
        color = "0.6"
    )

    plt.title("Median RT by Confidence Level")
    plt.xlabel("Confidence Rating")
    plt.ylabel("Median Reaction Time (s)")
    plt.tight_layout()
    plt.show()

### ==================== STEP 3: EXECUTE ALL ==================== ###

if __name__ == "__main__":
    ### ==================== Prep ==================== ###

    # gimme dataframe :3
    loaded_data = load_data("grating2AFC S11.mat")

    # {insert dataframe}.shape returns (rows, columns)
    # [0] is to extract number of rows
    total_trials = loaded_data.shape[0]
    # Why not half_trials, instead of first_half_trials? Because in cases where
    # trial numbers are odd, the first and second "half" would not be the same number.
    # // floors the division, so it will always be exactly half or possibly less
    first_half_trials = total_trials // 2

    ### ==================== 1.1 ==================== ###

    # RTs bar chart comparing first + second halves of experiment, with SEM error
    # bars
    #task_1_1(loaded_data, first_half_trials)

    ### ==================== 1.2 ==================== ###

    # T-test to see if RTs for the first and second half of the experiment differed
    # significantly.
    p_val = task_1_2(loaded_data, total_trials, first_half_trials)
    print(
        f"p-value: {p_val:.3g}\n"
        "Using a metric of minimal significance at p <= 0.05, "
        "if this were displayed with a bar-chart, there would be a bracket with "
        "two asterisks (**) above it — as the p-val is less than 0.01. This is a "
        "significant result."
    )

    ### ==================== 1.3 ==================== ###

    # Filtering out invalid data for confidence (negative numbers)
    valid_data = loaded_data[loaded_data["rating"] > 0]

    # Medians bar chart comparing between confidence levels of 1-4
    task_1_3(valid_data)


