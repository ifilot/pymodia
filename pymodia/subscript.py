def subscript(string_in):
    """
    Function to turn all numbers in string to subscript
    """
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    string_out = string_in.translate(SUB)

    return string_out
