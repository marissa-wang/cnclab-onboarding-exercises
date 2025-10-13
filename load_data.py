#!/usr/bin/env python
import pandas as pd
import scipy
from matplotlib import pyplot as plt
from rich import print


class TrialData:
    def __init__(self, fn: str):
        mat = scipy.io.loadmat(fn)
        data = mat["data"]
        stim_id = data["stimID"][0][0]  # 1 row, 1000 columns
        response = data["response"][0][0]
        rating = data["rating"][0][0]
        response_rt = data["responseRT"][0][0]
        self._df = pd.DataFrame(
            {
                "stimID": stim_id[0],  # 1000 columns
                "response": response[0],
                "rating": rating[0],
                "responseRT": response_rt[0],
            }
        )
        self._num_pts = self._df.shape[0]

    def task_1_1(self):
        # 1. Plot mean reaction times for the first half of the experiment.
        half_pts = int(self._num_pts / 2)
        first_half_data = self._df["responseRT"].head(half_pts)
        first_mean = first_half_data.mean()
        first_sem = first_half_data.sem()
        # 2. Do the same for second half of the experiment.
        second_half_data = self._df["responseRT"].tail(self._num_pts - half_pts)
        second_mean = second_half_data.mean()
        second_sem = second_half_data.sem()
        print(first_sem, second_sem)
        # 3. Put error bars (standard error of mean) on the two bars representing
        # the reaction times.
        # sns.barplot(x="Experiments", y="Mean RT", data=data)
        plt.bar(
            ["First Half", "Second Half"],
            [first_mean, second_mean],
            yerr=[first_sem, second_sem],
            capsize=5,
            color="skyblue",
            edgecolor="black",
        )
        plt.show()
        # 4. Put labels and everything to make it look nice. Make the graph
        # black and white only, and print it out.


def main():
    data = TrialData("grating2AFC S11.mat")
    data.task_1_1()


if __name__ == "__main__":
    main()
