def print_warning():
    print("Note: Creating trees with a high degree and depth is very taxing for your computer!")

def ask(text_prompt, correct_type_function, *args):
    while True:
        output = input(text_prompt + "\n")
        if correct_type_function(output, *args):
            break
    return output

def is_integer(string: str):
    return str.isdigit(string)

def higher_integer(string: str, previous_integer: int):
    return is_integer(string) and previous_integer <= int(string)

def is_tree_type(string: str):
    correct_answers = ["cayley_tree", "random_spanning_tree"]
    return string in correct_answers

def is_graph_type(string: str):
    correct_answers = ["cdf", "pdf", "spectral"]
    return string in correct_answers

def is_boolean(string: str):
    correct_answers = ["true", "false"]
    return str.lower(string) in correct_answers