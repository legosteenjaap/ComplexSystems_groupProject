import numpy as np
import matplotlib.pyplot as plt
import re
import os
import internal.questions as questions
import find_eigenvalues
import internal.cayley_tree_matrix as cayley_tree_matrix

"""
Python script that generated the graphs for our report for complex systems about tree networks.
"""

class InvalidFileNameException(Exception):
    pass

def find_numbers_in_file_name(file_name):
    re_pattern = r'\d+'
    return re.findall(re_pattern, str(file_name))

def load_data_files(directory):
    for file_name in os.listdir(directory):
            print(file_name + ", Loaded!")

            if "cayley_tree" in file_name:
                network_type = "cayley_tree"
            elif "random_spanning_tree" in file_name:
                network_type = "random_spanning_tree"
            else:
                raise InvalidFileNameException
            
            if network_type == "cayley_tree":
                degree, depth = find_numbers_in_file_name(file_name)
            else:
                depth = find_numbers_in_file_name(file_name)[0]
                degree = "-"
                
            data = np.genfromtxt(os.path.join (directory, file_name))

            yield network_type, degree, depth, data

def calculate_gap_and_nullity(eigenvalues, bin_width = 0.05):
    counts, bins = np.histogram(eigenvalues, bins=np.arange(min(eigenvalues), max(eigenvalues) + bin_width, bin_width))

    nullity = max(counts) / sum(counts)

    gap = 0
    chunk = counts[np.argmax(counts)+1:]
    while chunk[gap] == 0 and gap < len(chunk): 
        gap += 1
        
    return (gap * bin_width, nullity)

def save_figure(title):
    plt.savefig(os.path.join(current_directory, "graphs", title))

def generate_pdf_graph(network_type, degree, depth, eigenvalues):
    bin_width = 0.05
    plt.hist(eigenvalues, density=False, bins=np.arange(min(eigenvalues), max(eigenvalues) + bin_width, bin_width))
    plt.xlabel("Value")
    plt.ylabel("PDF")
    save_figure(f"pdf_graph_networktype_{network_type}_degree_{degree}_depth_{depth}.png")
    plt.close()

def generate_cdf_graph(network_type, degree, depth, eigenvalues):
    eigenvalues.sort()
    x_axis = np.linspace(0, 1, len(eigenvalues), endpoint=False)
    plt.plot(eigenvalues, x_axis)
    plt.xlabel("Value")
    plt.ylabel("CDF")
    save_figure(f"cdf_graph_networktype_{network_type}_degree_{degree}_depth_{depth}.png")
    plt.close()

def calculate_gaps_range(degree):
    gaps = []
    for depth in range (1, 7):
        matrix = cayley_tree_matrix.generate(degree=degree, depth=depth)
        
        eigenvalues = find_eigenvalues.find_eigen_values(matrix, False)
        gap, nullity = calculate_gap_and_nullity(eigenvalues)
        gaps.append(gap)
        print(f"Calculated gap for degree: {degree}, depth: {depth} with nullity: {nullity}!")
    return gaps


def generate_spectral_graph(is_comparison_graph):
    gaps_degree_3 = calculate_gaps_range(3)
    
    if is_comparison_graph:
        gaps_degree_4 = calculate_gaps_range(4)
        plt.plot(range(1,7), gaps_degree_3, label="Degree 3")
        plt.plot(range(1,7), gaps_degree_4, label="Degree 4")
        plt.legend(loc="best")
        plt.ylabel("Spectral gap")
        plt.xlabel("Graph depth")
        plt.title("Spectral gap vs graph depth for degrees = {3,4}")   
    else:
        plt.plot(range(1, 7), gaps_degree_3)
        plt.ylabel("Spectral gap")
        plt.xlabel("Graph depth")
        plt.title("Spectral gap vs graph depth for degree = 3")

    save_figure(f"spectral_graph_comparison_{is_comparison_graph}.png")

if __name__ == "__main__":

    current_directory = os.path.dirname(__file__)

    if not os.path.exists(os.path.join(current_directory, "graphs")): 
        os.mkdir(os.path.join(current_directory, "graphs"))

    print("---")
    print("This program will generate the PDF and CDF graphs for our report.")
    print("To generate these graphs you will first need to generate the eigenvalues with \"find_eigenvalues.py\"")
    print("---")

    graph_type = questions.ask("What type of graph do you want to generate? [pdf, cdf, spectral]", questions.is_graph_type)

    if graph_type == "pdf" or graph_type == "cdf":
        for network_type, degree, depth, eigenvalues in load_data_files(os.path.join(current_directory, "data")):
            if graph_type == "pdf":
                generate_pdf_graph(network_type, degree, depth, eigenvalues)
            elif graph_type == "cdf":
                generate_cdf_graph(network_type, degree, depth, eigenvalues)

    elif graph_type == "spectral":

        is_comparison_graph = questions.ask("Do you want a comparison between degree 3 and 4?", questions.is_boolean).lower() == "true"

        generate_spectral_graph(is_comparison_graph)

    print("Successfully created your graph(s)!")
