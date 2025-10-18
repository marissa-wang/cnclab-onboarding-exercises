import numpy as np
from scipy.stats import norm

def calc_d_prime(stim, resp):
    """
    Compute d′ directly from stimulus IDs and responses.
    Filters out invalid responses automatically.

    :param stim: 0 = noise (left), 1 = signal (right)
    :param resp: 0 = said 'left', 1 = said 'right', <0 = invalid (ignored)
    :return: d-prime value (float)
    """

    # Calculations here are based off of the equations
    # d' = Z(hit rate) - Z(false hit rate)
    # with Z() being finding the relevant z-score

    # Filter out invalid responses (negative codes)
    valid_mask = resp >= 0
    stim = stim[valid_mask]
    resp = resp[valid_mask]

    # Count hits and false hits
    #### only trials where stimulus and response aligned at 1
    hits = np.sum((stim == 1) & (resp == 1))
    #### all trials where the stimulus was 1
    total_signal = np.sum(stim == 1)
    #### only trials where stimulus was not there (0) and respondent chose 1
    false_hits = np.sum((stim == 0) & (resp == 1))
    #### all trials where the stimulus was 0
    total_noise = np.sum(stim == 0)

    # Edge case: no signal or noise trials in this subset :(
    if total_signal == 0 or total_noise == 0:
        return np.nan

    # Calculate rates (turns them into 0 <= value <= 1)
    hit_rate = hits / total_signal
    false_hits_rate = false_hits / total_noise

    # Calculate final d′
    # .ppf is (percent point function); finds what z-score it’s supposed to be
    # assuming a standard normal curve (mean = 0, sd = 1)
    z_hit_rate = norm.ppf(hit_rate)
    z_false_hit_rate = norm.ppf(false_hits_rate)

    return z_hit_rate - z_false_hit_rate