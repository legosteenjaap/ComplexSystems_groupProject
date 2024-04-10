import numpy as np
import scipy
from scipy import sparse
import matplotlib.pyplot as plt
import time
import os

"""
Python script for Complex Systems group project (rivers)    
"""

#this is the directed sparse version
#(the idear of sparce is that you can calculate bigger sizes matrixes, don't know actualy works)
def generate_adjacency_matrix_sparse(degree=3, depth=10):
    #(so when choosing depth of 0 => 1 node with no connections)

    #calc size matrix
    size_matrix = calc_size_matrix(degree, depth)

    #total amount of nodes that are connected to an other node
    size_connected_points = calc_size_matrix(degree, depth - 1)

    index_row = np.zeros(size_matrix - 1)
    index_col = np.zeros(size_matrix - 1)
    data = np.ones(size_matrix - 1)

    index_counter = 0

    #populate matrix
    y_cordinates_counter = 1
    for i in range(size_connected_points):
        if i == 0:
            for j in range(degree):
                index_row[index_counter] = y_cordinates_counter + j
                index_col[index_counter] = i
                index_counter += 1
            y_cordinates_counter += degree
        else:
            for j in range(degree - 1):
                index_row[index_counter] = y_cordinates_counter + j
                index_col[index_counter] = i
                index_counter += 1
            y_cordinates_counter += degree - 1
                
    # base_matrix = sparse.coo_matrix((data, (index_row, index_col)), shape=(size_matrix, size_matrix), dtype=np.int8).toarray()
    # base_matrix = sparse.coo_matrix((data, (index_row, index_col)), shape=(size_matrix, size_matrix)).toarray()
    base_matrix = sparse.coo_matrix((data, (index_row, index_col)), shape=(size_matrix, size_matrix))
    return base_matrix

#this is the directed non sparce version
def generate_adjacency_matrix_np_version(degree=3, depth=15):
    #(so when choosing depth of 0 => 1 node with no connections)

    #calc size matrix
    size_matrix = calc_size_matrix(degree, depth)

    base_matrix = np.zeros((size_matrix,size_matrix))

    #total amount of nodes that are connected to an other node
    size_connected_points = calc_size_matrix(degree, depth - 1)

    #populate matrix
    y_cordinates_counter = 1
    for i in range(size_connected_points):
        if i == 0:
            for j in range(degree):
                base_matrix[y_cordinates_counter + j, i] = 1
            y_cordinates_counter += degree
        else:
            for j in range(degree - 1):
                base_matrix[y_cordinates_counter + j, i] = 1
            y_cordinates_counter += degree - 1
                
    return base_matrix

def generate_bidirectional_matrix_sparse(degree=3, depth=10):
    matrix_1 = generate_adjacency_matrix_sparse(degree, depth)
    matrix_1t = np.transpose(matrix_1)
    return matrix_1 + matrix_1t

def generate_bidirectional_matrix_np_version(degree=3, depth=10):
    matrix_1 = generate_adjacency_matrix_np_version(degree, depth)
    matrix_1t = np.transpose(matrix_1)
    return matrix_1 + matrix_1t

def calc_size_matrix(degree, depth):
    if depth == 0:
        return 1  #(origin point)

    elif depth == 1:
        return 1 + degree

    else:
        total_value = 1 + degree
        outer_nodes = degree         
        
        for i in range(depth - 1):
            outer_nodes = outer_nodes * (degree - 1)
            total_value += outer_nodes
        return total_value




#just a function that prints a table to terminal, to give you an impression of 
# the different matrix sizes and different depths
def show_sizes(max_depth=10):
    print(f"size \t split=3 \t split=4")
    for i in range(max_depth+1):
        print(f"{i} \t {calc_size_matrix(3, i)} \t {calc_size_matrix(4, i)}")


def eigenvalues_sparse(degree, depth):
    start_time = time.time()
    temp_matrix = generate_bidirectional_matrix_sparse(degree=degree, depth=depth)
    temp_size_matrix = temp_matrix.shape[0]
    eigenvalues, eigenvectors = scipy.sparse.linalg.eigs(temp_matrix, k=temp_size_matrix-2)
    end_time = time.time()

    diff_time = end_time - start_time

    return eigenvalues, diff_time

def eigenvalues_non_sparse(degree, depth):
    start_time = time.time()
    temp_matrix = generate_bidirectional_matrix_np_version(degree=degree, depth=depth)
    temp_size_matrix = temp_matrix.shape[0]
    eigenvalues, eigenvectors = np.linalg.eig(temp_matrix)
    end_time = time.time()

    diff_time = end_time - start_time

    return eigenvalues, diff_time

# (be cautious choosing values bigger than 10, for split rate 3)
def calc_and_safe_data(depth_beginning, depth_end, degree):

    for depth in range(depth_beginning, depth_end + 1): #(is +1 correct?)
        #choose which method (sparse or non sparse [nonsparse seems to be faster...])
        eigenvalues, time = eigenvalues_non_sparse(depth=depth, degree=degree)
        # eigenvalues, time = eigenvalues_sparse(depth=depth, degree=degree)
    
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


