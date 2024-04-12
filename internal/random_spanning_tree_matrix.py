import networkx as nx

def get_amount_of_nodes(depth):
    amount_of_nodes = 0
    previous_layer_nodes = 3
    
    for i in range(2, depth + 1):
        current_layer_nodes = 2 * previous_layer_nodes
        amount_of_nodes += current_layer_nodes
        previous_layer_nodes= current_layer_nodes
    
    amount_of_nodes += 4
    
    return amount_of_nodes

def generate(depth, is_sparse=False):
    random_spanning_tree_network = nx.random_spanning_tree(nx.complete_graph(get_amount_of_nodes(depth)))
    return nx.adjacency_matrix(random_spanning_tree_network).toarray()