import numpy as np
import scipy
from scipy import sparse
import cayley_tree_matrix
import matplotlib.pyplot as plt
import time
import os

"""
Python script for Complex Systems group project (rivers)    
"""



def eigenvalues_sparse(degree, depth):
    start_time = time.time()
    temp_matrix = cayley_tree_matrix.generate(degree=degree, depth=depth, is_sparse=True)
    temp_size_matrix = temp_matrix.shape[0]
    eigenvalues, eigenvectors = scipy.sparse.linalg.eigs(temp_matrix, k=temp_size_matrix-2)
    end_time = time.time()

    diff_time = end_time - start_time

    return eigenvalues, diff_time

def eigenvalues_non_sparse(degree, depth):
    start_time = time.time()
    temp_matrix = cayley_tree_matrix.generate(degree=degree, depth=depth)
    eigenvalues, eigenvectors = np.linalg.eig(temp_matrix)
    end_time = time.time()

    diff_time = end_time - start_time

    return eigenvalues, diff_time

# (be cautious choosing values bigger than 10, for split rate 3)
def calc_and_safe_data(depth_beginning, depth_end, degree):

    for depth in range(depth_beginning, depth_end + 1): #(is +1 correct?)
        #choose which method (sparse or non sparse [nonsparse seems to be faster...])
        eigenvalues, time = eigenvalues_non_sparse(depth=depth, degree=degree)
        #eigenvalues, time = eigenvalues_sparse(depth=depth, degree=degree)
    
        print(f"current_settings, degree={degree}, depth={depth}")
        print(f"Time passed: {time}")
        print(f"Eigenvalues: (amount: {len(eigenvalues)})")
        # print(eigenvalues)

        #WARNING: I convert here numpy array to real part of array
        #I beleave there is no complex part and this should be fine.
        #I do this because of very small errors convert the real numbers in to complex.
        eigenvalues = np.real(eigenvalues)

        #safe file here (you need to run the code from the project root)
        if not os.path.exists("data"): os.mkdir("data")
        np.savetxt(f"data/eigenvalues_split_{degree}_depth_{depth}.txt", eigenvalues)



if __name__ == "__main__":
    # from sys import getsizeof

    #some old code lines
    # temp_matrix = sparse.csr_matrix(temp_matrix)
    # temp_matrix = temp_matrix.todense()
    
    print("Strating Complex Systems group project (rivers)")
    print("The main file now only generates data files.")

    #test data generation (later remove this part)
    # calc_and_safe_data(4, 6, 3)

    #data generation (later uncomment this part)
    calc_and_safe_data(10, 14, 2)
    calc_and_safe_data(4, 13, 3)
    calc_and_safe_data(4, 8, 4)
    calc_and_safe_data(4, 5, 5)

    #make plots
    # show matrix adjecancy form
    # plt.spy(temp_matrix)
    # plt.show()
    
    # show eigenvalues (sorted)
    # eigenvalues.sort()
    # plt.plot(eigenvalues)
    # plt.ylabel("eigenvalues")
    # plt.show()

    #show table with sizes
    # show_sizes(20)


