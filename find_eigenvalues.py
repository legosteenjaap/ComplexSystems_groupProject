import numpy as np
import scipy
import scipy.sparse
import scipy.sparse.linalg
import internal.questions as questions
import internal.cayley_tree_matrix as cayley_tree_matrix
import internal.random_spanning_tree_matrix as random_spanning_tree_matrix
import time
import os

"""
Python script for finding the eigenvalues of an adjacency matrix of a tree network.    
"""

def time_function(function, *args, **kwargs):
    """Records the amount of time that a function takes to execute"""
    start_time = time.time()
    result = function(*args, **kwargs)
    end_time = time.time()

    return result, (end_time - start_time)

def find_eigen_values(matrix, is_sparse):
    """Finds the eigen values for the given adjacency matrix"""
    if is_sparse:
        #Sadly can only find a few eigenvalues when using sparse matrices
        eigenvalues, eigenvectors = scipy.linalg.eig(matrix.todense())
    else:
        eigenvalues, eigenvectors = scipy.linalg.eig(matrix)
    
    #WARNING: I drop the complex part of the numpy array here, because it's probally negligible.
    eigenvalues = np.real(eigenvalues)
    
    return eigenvalues

def save_eigenvalues(degree, depth, network_type, eigenvalues):
    """Saves the given eigenvalues to disk with the right filename"""
    current_directory = os.path.dirname(__file__)
        
    if not os.path.exists(os.path.join(current_directory, "data")): 
        os.mkdir(os.path.join(current_directory, "data"))
        
    np.savetxt(os.path.join(current_directory, f"data/eigenvalues_networktype_{network_type}_degree_{degree}_depth_{depth}.txt"), eigenvalues)

def print_calculation_info(degree, depth, is_cayley, time, amount_of_eigenvalues):
    """Prints the info about the finished calculation on screen"""
    if is_cayley:
        print(f"current_settings, networktype=cayley_tree, degree={degree}, depth={depth}")
    else:
        print(f"current_settings, networktype=random_spanning_tree, depth={depth}")
    print(f"Time passed: {time}")
    print(f"Eigenvalues: (amount: {amount_of_eigenvalues})")

def calculate_data(depth, is_cayley, degree, is_sparse=False):
    """Calculates and saves the eigenvalue data on disk for one graph"""
    if is_cayley:
        matrix = cayley_tree_matrix.generate(degree=degree, depth=depth, is_sparse=is_sparse)
    else:
        matrix = random_spanning_tree_matrix.generate(depth)
        
    eigenvalues = find_eigen_values(matrix, is_sparse)

    network_type = "cayley_tree" if is_cayley else "random_spanning_tree"

    save_eigenvalues(degree, depth, network_type, eigenvalues)

    return eigenvalues

def calculate_data_multiple_depths(depth_beginning, depth_end, is_cayley, degree, is_sparse=False):
    """Calculates and saves the eigenvalue data on disk for multiple graphs"""
    for depth in range(depth_beginning, depth_end + 1):
        eigenvalues, time = time_function(calculate_data, depth, is_cayley, degree, is_sparse=is_sparse)
        print_calculation_info(degree, depth, is_cayley, time, len(eigenvalues))

if __name__ == "__main__":
    
    print("---")
    print("Starting eigenvalues calculator!")
    print("This program will find the eigenvalues for tree network adjacency matrices.")
    questions.print_warning()
    print("---")
    
    is_cayley = questions.ask("Which type of network do you want to generate [cayley_tree, random_spanning_tree]?", questions.is_tree_type) == "cayley_tree"
    if is_cayley:
        degree = int(questions.ask("Which degree of tree networks do you want to generate?", questions.is_integer))
    else:
        degree = "-"

    depth_start = int(questions.ask("At which depth do you want to start generating your trees?", questions.is_integer))
    depth_end = int(questions.ask("And at which depth do you want to stop?", questions.higher_integer, depth_start))

    is_sparse = False

    if is_cayley:
        is_sparse = (questions.ask("Do you want to use the sparse data structure for large adjacency matrices[True, False]? (only faster with very large matrices)", questions.is_boolean)).lower() == "true"

    calculate_data_multiple_depths(depth_start, depth_end, is_cayley, degree, is_sparse=is_sparse)

    print("Succesfully calculated all your eigenvalues!")

