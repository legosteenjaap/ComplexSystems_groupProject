import matplotlib.pyplot as plt
import internal.cayley_tree_matrix as cayley_tree_matrix
import internal.random_spanning_tree_matrix as random_spanning_tree_matrix
import networkx as nx
import internal.questions as questions
import os

"""
Python script for visualizing matrices and networks of cayley and random spanning trees.
"""

def save(file_name):
    """Saves the current figure to disk in the correct folder"""
    current_directory = os.path.dirname(__file__)
        
    if not os.path.exists(os.path.join(current_directory, "visualizations")): 
        os.mkdir(os.path.join(current_directory, "visualizations"))
    
    plt.savefig(os.path.join(current_directory, "visualizations", file_name))
    plt.close()

def visualize_matrix(file_name, matrix):
    """Visualizes an adjacency matrix"""
    plt.spy(matrix)
    plt.title(file_name)
    save(file_name)

def visualize_network(file_name, matrix, node_visualization_size, numbered_nodes):
    """Visualizes the tree network with networkx"""
    network = nx.DiGraph(matrix)
    nx.draw(network, node_size=node_visualization_size, arrows=False, with_labels=numbered_nodes)
    plt.title(file_name)
    save(file_name)

if __name__ == "__main__":
    
    print("---")
    print("This program wil draw simple graphs to visualize adjacency matrices for trees.")
    print("Hopefully this is usefull to understand them and make sure that they function properly.")
    print("Ones are displayed with black pixels and zeros with white pixels.")
    questions.print_warning()
    print("---")

    network_type = questions.ask("Which type of network do you want to generate [cayley_tree, random_spanning_tree]?", questions.is_tree_type)
    is_cayley = network_type == "cayley_tree"
    if is_cayley:
        degree = int(questions.ask("Which degree of Cayley tree do you want to generate?", questions.is_integer))
    else:
        degree = "-"
    
    depth = int(questions.ask("And what is the depth for your tree?", questions.is_integer))

    if is_cayley:
        matrix = cayley_tree_matrix.generate(degree=degree, depth=depth)
    else:
        matrix = random_spanning_tree_matrix.generate(depth)

    node_visualization_size = int(questions.ask("What size should the nodes be? [default:500]", questions.is_integer))
    numbered_nodes = (questions.ask("Do you want to number the nodes?", questions.is_boolean)).lower() == "true"

    visualize_matrix(f"matrix_visualization_networktype_{network_type}_degree_{degree}_depth_{depth}", matrix)
    visualize_network(f"network_visualization_networktype_{network_type}_degree_{degree}_depth_{depth}", matrix, node_visualization_size, numbered_nodes)

    print("Succesfully saved the visualization of the matrix and network of your tree!")