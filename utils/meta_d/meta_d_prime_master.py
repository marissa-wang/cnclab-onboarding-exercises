import warnings
import numpy as np
from contextlib import redirect_stdout
import os
from utils.meta_d.trials_to_counts import trials_to_counts
from utils.meta_d.fit_meta_d_MLE import fit_meta_d_MLE

def compute_meta_d_prime(data, n_ratings=4, pad_cells=1):
    """
    Compute meta-d' from a dataframe containing 'stimID', 'response', and 'rating'.

    :param data: pandas DataFrame
    :param n_ratings: number of confidence ratings (default 4)
    :param pad_cells: whether to pad counts to avoid log(0) issues
    :return: fit dict (meta_d', d', M_ratio, M_diff)
    """

    # number (of) responses (for) stimulus 1,
    # number (of) responses (for) stimulus 2
    nr_s1, nr_s2 = trials_to_counts(
        data['stimID'],
        data['response'],
        data['rating'],
        n_ratings,
        pad_cells=pad_cells # adds vals to all bins to prevent log(0) errors
    )

    # suppress warnings and optimizer chatter
    with open(os.devnull, 'w') as f, redirect_stdout(f):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            warnings.simplefilter("ignore", UserWarning)
            with np.errstate(invalid='ignore', divide='ignore'):
                fit = fit_meta_d_MLE(nr_s1, nr_s2)

    return fit