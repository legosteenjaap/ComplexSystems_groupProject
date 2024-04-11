import matplotlib.pyplot as plt
import cayley_tree_matrix
import os
import gen_graphs
import questions

dpi_setting = gen_graphs.dpi_setting

def visualize_matrix(title, matrix):
    plt.figure(dpi=dpi_setting)
    plt.spy(matrix)
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    
    current_directory = os.path.dirname(__file__)

    print("This program wil draw simple graphs to visualize Cayley treematrices.")
    print("Hopefully this is usefull to understand them and make sure that they function properly.")
    questions.print_warning()
    degree = int(questions.ask("Which degree of Cayley tree do you want to generate?", questions.is_integer))
    depth = int(questions.ask("And what is the depth for your Cayley tree?", questions.is_integer))

    visualize_matrix("Visualization test matrix ", cayley_tree_matrix.generate(degree=degree, depth=depth))