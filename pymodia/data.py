from typing import Any
from .molecule import MoDiaMolecule
from .fragment import MoDiaFragment

class MoDiaData():
    """
    Class that combines the data to make the molecular orbital diagram
    """
    def __init__(
        self,
        molecule: MoDiaMolecule,
        fragment1: MoDiaFragment,
        fragment2: MoDiaFragment,
        **kwargs: Any,
    ) -> None:
        """
        Initialize a MoDia data container.

        Parameters
        ----------
        molecule
            The molecule object containing molecular orbital energies,
            coefficients, and electron count.
        fragment1
            First molecular fragment (e.g. atom or group of atoms).
        fragment2
            Second molecular fragment.
        **kwargs
            Optional keyword arguments used to customize internal behavior
            or override default settings.
        """
        ...


        allowed_data = {'name', 'moe', 'orbc'}
        self.__dict__.update((k, v) for k, v in kwargs.items()
                             if k in allowed_data)

        self.molecule = molecule
        self.fragment1 = fragment1
        self.fragment2 = fragment2

        # When loading the molecular orbital (MO) energies, a copy is made of the
        # raw energies and used to set the energy labels. The user can now
        # overwrite the MO energies which will adjust the position where the
        # MOs are being plotted, but will conserve the energies. This allows
        # the user to make small adjustment to the energy levels to avoid
        # any form of overlapping.
        self.moe_labels = [float(e) for e in self.molecule.state_energies]

    def set_ao_energy(self, atom_index, energies):
        """
        Set the atomic orbital energies of atom 1 or atom 2

        Parameters
        ----------
        atom_index : int
            either 0 or 1 corresponding to setting energies of either atom 1
            or 2 respectively
        energies : lst
            list of two lists with the energies of atoms 1 and 2

        """
        if atom_index == 0:
            self.atom1.e = energies
        elif atom_index == 1:
            self.atom2.e = energies
        else:
            raise Exception("atom_index must be either 0 or 1")

        return self

    def set_ao_energies(self, energies):
        """
        Set the atomic orbital energies of atom 1 and atom 2

        Parameters
        ----------
        energies : lst
            list of two lists with the energies of atoms 1 and 2

        """

        self.atom1.e = energies[0]
        self.atom2.e = energies[1]

        return self

    def set_moe(self, moe):
        """
        Overwrite MO energies. Used to adjust the position of the MO energies
        in the diagram while retaining the actual energy values.

        Parameters
        ----------
        moe : lst
            List of MO energies
        """
        self.molecule.state_energies = moe

        return self

    def from_json(self, json):
        """
        Reads json file and import data

        Parameters
        ----------
        json
            file path to json file with data

        """
        pass

    def save_json(self, path):
        """
        Saves data from MoDiaData object to json file

        Parameters
        ----------
        path
            path to save json file to

        """
        pass