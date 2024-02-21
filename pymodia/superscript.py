def superscript(string_in):
    """
    Function to turn all numbers with ^in front in string to superscript
    """
    sup = False
    string_out = ""
    for element in string_in:
        if sup == True:
            SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
            sup_element = element.translate(SUP)
            sup = False
            string_out += sup_element
        elif element == "^":
            sup = True
        else:
            string_out += element

    return string_out
