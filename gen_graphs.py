import main
import numpy as np
import scipy
from scipy import sparse
import matplotlib.pyplot as plt
import time
import pathlib
import re

dpi_setting = 150


def load_data_files():
    data_loc = pathlib.Path("data")
    for item in data_loc.iterdir():
        if item.is_file():
            print(item)

            #get type data
            re_pattern = r'\d+'
            split_rate, depth = re.findall(re_pattern, str(item))

            #load data
            # data = np.genfromtxt(f"graphs/{item}")
            data = np.genfromtxt(item)
            # data = np.loadtxt(item)
            # print(data)
            yield split_rate, depth, data
            

#Here generate graphs from  main.py data.
if __name__ == "__main__":

    #show form matrix
    # show matrix adjecancy form
    temp_matrix1 = main.generate_bidirectional_matrix_np_version(split_rate=3, depth=3)
    temp_matrix2 = main.generate_bidirectional_matrix_np_version(split_rate=4, depth=2)
    plt.figure(dpi=dpi_setting)
    plt.spy(temp_matrix1)
    plt.savefig("graphs/matrix_layout1.png")
    plt.figure(dpi=dpi_setting)
    plt.spy(temp_matrix2)
    plt.savefig("graphs/matrix_layout2.png")


    #genegrate graphs based on data
    for split_rate, depth, eigenvalues in load_data_files():

        #make histplot:
        bins = int(np.sqrt(len(eigenvalues)))
        if bins % 2 == 0: #(make shure is uneaven)
            bins += 1
        #temp adjustment:
        dubbel_bins = (bins -1) * 4 + 1
        #sqrt(N) graph
        plt.figure(dpi=dpi_setting)
        plt.hist(eigenvalues, bins=bins)
        plt.ylabel("amount of eigenvalue")
        plt.xlabel("eigenvalues")
        plt.savefig(f"graphs/hist_plot_split_{split_rate}_depth_{depth}.png")
        #dubbel bins (for now disabled)
        # plt.figure(dpi=dpi_setting)
        # plt.hist(eigenvalues, bins=dubbel_bins)
        # plt.ylabel("amount of eigenvalue")
        # plt.xlabel("eigenvalues")
        # plt.savefig(f"graphs/hist_plot_dubbel_bins_split_{split_rate}_depth_{depth}.png")
        
        # show eigenvalues (sorted)
        eigenvalues.sort()
        x_axis = np.arange(len(eigenvalues)) / len(eigenvalues)
        plt.figure(dpi=dpi_setting)
        plt.plot(x_axis, eigenvalues)
        plt.scatter(x_axis, eigenvalues, s=2)
        plt.ylabel("eigenvalues")
        plt.xlabel("relative index of sorted eigenvalues")
        plt.savefig(f"graphs/sorted_line_plot_split_{split_rate}_depth_{depth}.png")


