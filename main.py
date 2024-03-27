import numpy as np

"""
Python script for Complex Systems group project (rivers)    
"""

#this is the directed version
def generate_adjacency_matrix(split_rate=3, depth=15):
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

def generate_bidirectional_matrix(split_rate=3, depth=10):
    matrix_1 = generate_adjacency_matrix(split_rate, depth)
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
# the different matrix sizes ad different depths
def show_sizes(max_depth=10):
    print(f"size \t split=3 \t split=4")
    for i in range(max_depth+1):
        print(f"{i} \t {calc_size_matrix(3, i)} \t {calc_size_matrix(4, i)}")


if __name__ == "__main__":
    print("Strating Complex Systems group project (rivers)")

    print(generate_bidirectional_matrix(depth=2))

    show_sizes(20)



