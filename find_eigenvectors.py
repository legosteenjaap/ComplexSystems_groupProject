import numpy as np
import scipy
import ComplexSystems_groupProject.internal.questions as questions
import ComplexSystems_groupProject.internal.cayley_tree_matrix as cayley_tree_matrix
import time
import os

"""
Python script for finding the eigenvectors of an adjacency matrix of a Cayley tree.    
"""

def time_function(function, *args, **kwargs):
    """Records the amount of time that a function takes to execute"""
    start_time = time.time()
    result = function(*args, **kwargs)
    end_time = time.time()
    return result, (end_time - start_time)

def find_eigen_values(matrix):
    """Finds the eigen values for the given adjacency matrix"""
    eigenvalues, eigenvectors = scipy.linalg.eig(matrix)
    
    #WARNING: I drop the complex part of the numpy array here, because it's probally negligible.
    eigenvalues = np.real(eigenvalues)
    
    return eigenvalues

def save_eigenvalues(degree, depth, eigenvalues):
    current_directory = os.path.dirname(__file__)
        
    if not os.path.exists(os.path.join(current_directory, "data")): 
        os.mkdir(os.path.join(current_directory, "data"))
        
    np.savetxt(os.path.join(current_directory, f"data/eigenvalues_degree_{degree}_depth_{depth}.txt"), eigenvalues)

def print_calculation_info(degree, depth, time, amount_of_eigenvalues):
    """Prints the info about the finished calculation on screen"""
    print(f"current_settings, degree={degree}, depth={depth}")
    print(f"Time passed: {time}")
    print(f"Eigenvalues: (amount: {amount_of_eigenvalues})")

def calculate_and_save_data(depth_beginning, depth_end, degree, is_sparse=False):
    """Calculates and saves the data on disk for multiple graphs with certain degrees"""
    for depth in range(depth_beginning, depth_end + 1):
        
        matrix = cayley_tree_matrix.generate(degree=degree, depth=depth, is_sparse=is_sparse)
        eigenvalues, time = time_function(find_eigen_values, matrix)

        save_eigenvalues(degree, depth, eigenvalues)

        print_calculation_info(degree, depth, time, len(eigenvalues))

if __name__ == "__main__":
    
    print("Starting eigenvector calculator!")
    print("This program will find the eigenvectors for Caylee tree adjacency matrices.")
    questions.print_warning()
    degree = int(questions.ask("Which degree of Cayley trees do you want to generate?", questions.is_integer))
    depth_start = int(questions.ask("At which depth do you want to start generating Cayley trees?", questions.is_integer))
    depth_end = int(questions.ask("And at which depth do you want to stop?", questions.higher_integer, depth_start))

    calculate_and_save_data(depth_start, depth_end, degree)

