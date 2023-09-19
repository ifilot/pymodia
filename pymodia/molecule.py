class Molecule():
    """
    Class that combines the information about a molecule needed to make the
    MO diagram
    """

    def __init__(self, Name, Atom1, count_atom_1, Atom2, count_atom_2):
        self.name = Name
        self.a1 = Atom1
        self.nr_a1 = count_atom_1
        self.a2 = Atom2
        self.nr_a2 = count_atom_2
