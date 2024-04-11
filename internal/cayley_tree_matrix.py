import numpy as np
from scipy import sparse

def get_amount_of_nodes(degree, depth):
    """Calculates the amount of nodes for the cayley tree with the given degree and depth"""
    if depth < 0:
        #Otherwise the code crashes when generating a tree with depth 0
        return 0 
    elif depth == 0:
        #If the depth is zero we only have one center node
        return 1
    elif depth == 1:
        return 1 + degree 
    else:
        matrix_size = 1 + degree
        next_layer_nodes = degree         
        
        for i in range(depth - 1):
            next_layer_nodes = next_layer_nodes * (degree - 1)
            matrix_size += next_layer_nodes
        return matrix_size

def fill_normal_matrix(matrix, row_pos, column_pos):
    """Stores the data on a normal matrix"""
    matrix[row_pos, column_pos] = 1

class SparseData:
    """Simple class for storing sparse matrix data temporarely"""

    def __init__(self, matrix_size):
        self.row_positions = np.zeros(matrix_size - 1)
        self.column_positions = np.zeros(matrix_size - 1)
        self.index = 0
    
    def get_row_positions(self):
        return self.row_positions
    
    def get_column_positions(self):
        return self.column_positions
    
    def get_index(self):
        return self.index
    
    def increment_index(self):
        self.index +=1


def fill_special_sparse_matrix(sparse_matrix : SparseData, row_pos, column_pos):
    """Stores the data for the special data structure which can hold sparse matrices"""
    sparse_matrix.row_positions[sparse_matrix.get_index()] = row_pos
    sparse_matrix.column_positions[sparse_matrix.get_index()] = column_pos
    sparse_matrix.increment_index()

def finalize_special_sparse_matrix(sparse_matrix: SparseData, matrix_size):
    """Converts the SparseData to a sparse matrix from the scipy module"""
    data = np.ones(matrix_size - 1)
    return sparse.coo_matrix((data, (sparse_matrix.get_row_positions(), sparse_matrix.get_column_positions())), shape=(matrix_size, matrix_size))

def initialize_matrix(matrix_size, is_sparse):
    """Initializes cayley tree matrix"""

    if is_sparse:
        fill_function = fill_special_sparse_matrix

        matrix = SparseData(matrix_size)
    else:
        fill_function = fill_normal_matrix

        matrix = np.zeros((matrix_size, matrix_size))

    return matrix, fill_function

def fill_matrix(matrix, fill_function, degree, depth):
    """Fills the adjacency matrix with the data for the cayley tree
        Note: To understand this algorithm run the file called \"visualize_matrix.py\" to see a visual representation of the generated matrix"""

    #Amount of nodes that aren't on the outside of the tree a.k.a non leaf nodes
    non_leaf_node_amount = get_amount_of_nodes(degree, depth - 1)

    current_column = 1
    for i in range(non_leaf_node_amount):
        next_layer_nodes = (degree - 1) if i !=0 else degree
        
        for j in range(next_layer_nodes):
            fill_function(matrix, i, current_column + j)
        
        current_column += next_layer_nodes
    return matrix

def get_bi_directional(matrix):
    """Returns a symmetric version of the matrix by adding it up with it's transposed version"""
    return matrix + np.transpose(matrix)

def generate(degree=3, depth=10, is_sparse=False, is_bi_directional=True):
    """Generates an adjacency matrix for a cayley tree
        Arguments:
            degree (int): The degree of all non leaf nodes on the cayley tree
            depth (int): The distance from the center at which the cayley tree ends and it's leaves generate
            is_sparse (bool): Records if the cayley tree should be stored in memory with a special data structure for sparse matrices or not
            is_bi_directional (bool): Records if the matrix should be made symmetric by adding it up with it's transposed variant"""
    
    matrix_size = get_amount_of_nodes(degree, depth)

    matrix, fill_function = initialize_matrix(matrix_size, is_sparse)

    matrix = fill_matrix(matrix, fill_function, degree, depth)

    if is_sparse:
        matrix = finalize_special_sparse_matrix(matrix, matrix_size)

    if is_bi_directional:
        return get_bi_directional(matrix)

    return matrix