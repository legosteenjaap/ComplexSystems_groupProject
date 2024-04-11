def print_warning():
    print("Note: Calculating Cayley trees with a high degree and depth is very taxing for your computer")

def ask(text_prompt, correct_type_function, *args):
    while True:
        output = input(text_prompt)
        if correct_type_function(output, *args):
            break
    return output

def is_integer(string: str):
    return str.isdigit(string)

def higher_integer(string: str, previous_integer: int):
    return is_integer(string) and previous_integer <= int(string)