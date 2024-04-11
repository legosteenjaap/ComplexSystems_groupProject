import numpy as np
import matplotlib.pyplot as plt
import re
import os

dpi_setting = 150

def find_numbers_in_file_name(file_name):
    re_pattern = r'\d+'
    return re.findall(re_pattern, str(file_name))

def load_data_files(directory):
    for file_name in os.listdir(directory):
            print(file_name)

            degree, depth = find_numbers_in_file_name(file_name)

            data = np.genfromtxt(os.path.join (directory, file_name))

            yield degree, depth, data
            

#Here generate graphs from  main.py data.
if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    #genegrate graphs based on data
    for degree, depth, eigenvalues in load_data_files(os.path.join(current_directory, "data")):

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
        plt.savefig(os.path.join(current_directory, "graphs", "hist_plot_split_{degree}_depth_{depth}.png"))

        #dubbel bins (for now disabled)
        # plt.figure(dpi=dpi_setting)
        # plt.hist(eigenvalues, bins=dubbel_bins)
        # plt.ylabel("amount of eigenvalue")
        # plt.xlabel("eigenvalues")
        # plt.savefig(f"graphs/hist_plot_dubbel_bins_split_{degree}_depth_{depth}.png")
        
        # show eigenvalues (sorted)
        eigenvalues.sort()
        x_axis = np.arange(len(eigenvalues)) / len(eigenvalues)
        plt.figure(dpi=dpi_setting)
        plt.plot(x_axis, eigenvalues)
        plt.scatter(x_axis, eigenvalues, s=2)
        plt.ylabel("eigenvalues")
        plt.xlabel("relative index of sorted eigenvalues")
        plt.savefig(os.path.join(current_directory, f"graphs/sorted_line_plot_split_{degree}_depth_{depth}.png"))


