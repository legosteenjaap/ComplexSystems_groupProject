import numpy as np
import scipy
from scipy import sparse
import matplotlib.pyplot as plt
import time

"""
Python script for Complex Systems group project (rivers)    
"""

#this is the directed sparse version
#(the idear of sparce is that you can calculate bigger sizes matrixes, don't know actualy works)
def generate_adjacency_matrix_sparse(split_rate=3, depth=10):
    #(so when choosing depth of 0 => 1 node with no connections)

    #calc size matrix
    size_matrix = calc_size_matrix(split_rate, depth)

    #total amount of nodes that are connected to an other node
    size_connected_points = calc_size_matrix(split_rate, depth - 1)

    index_row = np.zeros(size_matrix - 1)
    index_col = np.zeros(size_matrix - 1)
    data = np.ones(size_matrix - 1)

    index_counter = 0

    #populate matrix
    y_cordinates_counter = 1
    for i in range(size_connected_points):
        if i == 0:
            for j in range(split_rate):
                index_row[index_counter] = y_cordinates_counter + j
                index_col[index_counter] = i
                index_counter += 1
            y_cordinates_counter += split_rate
        else:
            for j in range(split_rate - 1):
                index_row[index_counter] = y_cordinates_counter + j
                index_col[index_counter] = i
                index_counter += 1
            y_cordinates_counter += split_rate - 1
                
    # base_matrix = sparse.coo_matrix((data, (index_row, index_col)), shape=(size_matrix, size_matrix), dtype=np.int8).toarray()
    # base_matrix = sparse.coo_matrix((data, (index_row, index_col)), shape=(size_matrix, size_matrix)).toarray()
    base_matrix = sparse.coo_matrix((data, (index_row, index_col)), shape=(size_matrix, size_matrix))
    return base_matrix

#this is the directed non sparce version
def generate_adjacency_matrix_np_version(split_rate=3, depth=15):
    #(so when choosing depth of 0 => 1 node with no connections)

    #calc size matrix
    size_matrix = calc_size_matrix(split_rate, depth)

    base_matrix = np.zeros((size_matrix,size_matrix))

    #total amount of nodes that are connected to an other node
    size_connected_points = calc_size_matrix(split_rate, depth - 1)

    #populate matrix
    y_cordinates_counter = 1
    for i in range(size_connected_points):
        if i == 0:
            for j in range(split_rate):
                base_matrix[y_cordinates_counter + j, i] = 1
            y_cordinates_counter += split_rate
        else:
            for j in range(split_rate - 1):
                base_matrix[y_cordinates_counter + j, i] = 1
            y_cordinates_counter += split_rate - 1
                
    return base_matrix

def generate_bidirectional_matrix_sparse(split_rate=3, depth=10):
    matrix_1 = generate_adjacency_matrix_sparse(split_rate, depth)
    matrix_1t = np.transpose(matrix_1)
    return matrix_1 + matrix_1t

def generate_bidirectional_matrix_np_version(split_rate=3, depth=10):
    matrix_1 = generate_adjacency_matrix_np_version(split_rate, depth)
    matrix_1t = np.transpose(matrix_1)
    return matrix_1 + matrix_1t

def calc_size_matrix(split_rate, depth):
    if depth == 0:
        return 1  #(origin point)

    elif depth == 1:
        return 1 + split_rate

    else:
        total_value = 1 + split_rate
        outer_nodes = split_rate         
        
        for i in range(depth - 1):
            outer_nodes = outer_nodes * (split_rate - 1)
            total_value += outer_nodes
        return total_value




#just a function that prints a table to terminal, to give you an impression of 
# the different matrix sizes and different depths
def show_sizes(max_depth=10):
    print(f"size \t split=3 \t split=4")
    for i in range(max_depth+1):
        print(f"{i} \t {calc_size_matrix(3, i)} \t {calc_size_matrix(4, i)}")


def eigenvalues_sparse(split_rate, depth):
    start_time = time.time()
    temp_matrix = generate_bidirectional_matrix_sparse(split_rate=split_rate, depth=depth)
    temp_size_matrix = temp_matrix.shape[0]
    eigenvalues, eigenvectors = scipy.sparse.linalg.eigs(temp_matrix, k=temp_size_matrix-2)
    end_time = time.time()

    diff_time = end_time - start_time

    return eigenvalues, diff_time

def eigenvalues_non_sparse(split_rate, depth):
    start_time = time.time()
    temp_matrix = generate_bidirectional_matrix_np_version(split_rate=split_rate, depth=depth)
    temp_size_matrix = temp_matrix.shape[0]
    eigenvalues, eigenvectors = np.linalg.eig(temp_matrix)
    end_time = time.time()

    diff_time = end_time - start_time

    return eigenvalues, diff_time



if __name__ == "__main__":
    # from sys import getsizeof

    #some old code lines
    # temp_matrix = sparse.csr_matrix(temp_matrix)
    # temp_matrix = temp_matrix.todense()
    
    print("Strating Complex Systems group project (rivers)")

    #Set variables
    depth = 6  #(be cautious choosing values bigger than 10)
    split_rate = 3
    

    #choose which method (sparse or non sparse [nonsparse seems to be faster...])
    # eigenvalues, time = eigenvalues_non_sparse(depth=depth, split_rate=split_rate)
    eigenvalues, time = eigenvalues_sparse(depth=depth, split_rate=split_rate)

    print(f"Time passed: {time}")
    print(f"Eigenvalues: (amount: {len(eigenvalues)})")
    print(eigenvalues)


    #make plots
    # show matrix adjecancy form
    # plt.spy(temp_matrix)
    # plt.show()
    
    # show eigenvalues (sorted)
    eigenvalues.sort()
    plt.plot(eigenvalues)
    plt.ylabel("eigenvalues")
    plt.show()

    #show table with sizes
    # show_sizes(20)


