from . import Empty


class MoDiaMolecule():
    """
    Class that combines the information about a molecule needed to make the
    MO diagram
    """

    def __init__(self, Name, Atom1, count_atom_1, Atom2, count_atom_2):
        self.name = Name

        self.atom1 = Empty()
        self.atom1.name = Atom1.name
        self.atom1.e = Atom1.energies
        self.atom1.nr = count_atom_1
        self.atom1.atomic_number = Atom1.atomic_number
        self.atom1.configuration = Atom1.configuration

        self.atom2 = Empty()
        self.atom2.name = Atom2.name
        self.atom2.e = Atom2.energies
        self.atom2.nr = count_atom_2
        self.atom2.atomic_number = Atom2.atomic_number
        self.atom2.configuration = Atom2.configuration
