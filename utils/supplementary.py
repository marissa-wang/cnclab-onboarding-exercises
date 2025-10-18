import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
# custom import!
from main import load_data


def rolling_averages(data, first_half_trials, window=20, sigma=5):
    """
    Plot rolling averages (with Gaussian smoothing) for:
    - Hit Rate
    - False Alarm Rate
    - Confidence Ratings
    """

    # --- Rolling means ---
    conf_roll = data['rating'].rolling(window).mean()
    hit = ((data['stimID'] == 1) & (data['response'] == 1)).astype(int)
    fa = ((data['stimID'] == 0) & (data['response'] == 1)).astype(int)
    hit_roll = hit.rolling(window).mean()
    fa_roll = fa.rolling(window).mean()

    # --- Gaussian smoothing ---
    hit_smooth = gaussian_filter1d(hit_roll.bfill(), sigma=sigma)
    fa_smooth = gaussian_filter1d(fa_roll.bfill(), sigma=sigma)
    conf_smooth = gaussian_filter1d(conf_roll.bfill(), sigma=sigma)

    # --- Plot ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Top: Hit & FA
    ax1.plot(hit_smooth, label="Hit Rate", color="green")
    ax1.plot(fa_smooth, label="False Alarm Rate", color="red")
    ax1.axvline(first_half_trials, color='blue', linestyle='--', alpha=0.6)

    # Force draw before measuring limits
    plt.draw()
    ymin1, ymax1 = ax1.get_ylim()
    ax1.text(first_half_trials - 10, ymin1 + (ymax1 - ymin1) * 0.95,
             'Halfway', color='blue', fontsize=10, rotation=0, ha='right', va='top')

    ax1.set_ylabel("Hit / FA Rate")
    ax1.legend(loc="upper right")
    ax1.set_title(f"Rolling Hit / FA (window={window}, σ={sigma})")

    # Bottom: Confidence
    ax2.plot(conf_smooth, label="Confidence", color="black")
    ax2.axvline(first_half_trials, color='blue', linestyle='--', alpha=0.6)

    ymin2, ymax2 = ax2.get_ylim()
    ax2.text(first_half_trials - 10, ymin2 + (ymax2 - ymin2) * 0.95,
             'Halfway', color='blue', fontsize=10, rotation=0, ha='right', va='top')

    ax2.set_ylabel("Confidence (1–4)")
    ax2.set_xlabel("Trial")
    ax2.legend(loc="upper right")
    ax2.set_title(f"Rolling Confidence (window={window}, σ={sigma})")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":

    # gimme dataframe :3
    loaded_data = load_data("../grating2AFC S11.mat")

    # {insert dataframe}.shape returns (rows, columns)
    # [0] is to extract number of rows
    total_trials = loaded_data.shape[0]
    # Why not half_trials, instead of first_half_trials? Because in cases where
    # trial numbers are odd, the first and second "half" would not be the same number.
    # // floors the division, so it will always be exactly half or possibly less
    first_half_trials = total_trials // 2

    # Define valid ranges
    valid_stim_mask = loaded_data["stimID"].isin([0, 1])
    valid_resp_mask = loaded_data["response"].isin([0, 1])
    valid_rating_mask = loaded_data["rating"].between(1, 4)  # assuming 4-point confidence

    # Apply all filters at once
    valid_data = loaded_data[valid_stim_mask & valid_resp_mask & valid_rating_mask]

    rolling_averages(valid_data, first_half_trials)