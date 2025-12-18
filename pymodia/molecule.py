from . import Empty


class MoDiaMolecule():
    """
    Class that combines the information about a molecule needed to make the
    MO diagram
    """

    def __init__(self, name, energies):
        self.name = name
        self.energies = energies