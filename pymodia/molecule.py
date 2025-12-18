from . import Empty


class MoDiaMolecule():
    """
    Class that combines the information about a molecule needed to make the
    MO diagram
    """

    def __init__(self, name, state_energies, state_coefficients, nr_elec):
        self.name = name
        self.state_energies = state_energies
        self.state_coefficients = state_coefficients
        self.nelec = nr_elec