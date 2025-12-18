from . import Empty
import numpy as np


class MoDiaData():
    """
    Class that combines the data to make the molecular orbital diagram
    """

    def __init__(self, **kwargs):

        allowed_data = {'name', 'moe', 'orbc'}
        self.__dict__.update((k, v) for k, v in kwargs.items()
                             if k in allowed_data)

        if 'molecule' in kwargs:
            self.__set_molecule(kwargs['molecule'])

        # When loading the molecular orbital (MO) energies, a copy is made of the
        # raw energies and used to set the energy labels. The user can now
        # overwrite the MO energies which will adjust the position where the
        # MOs are being plotted, but will conserve the energies. This allows
        # the user to make small adjustment to the energy levels to avoid
        # any form of overlapping.
        if hasattr(self, "moe"):
            self.moe_labels = [float(e) for e in self.moe]

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
        self.moe = moe

        return self

    def __set_molecule(self, molecule):
        """
        Set the molecule data based on a MoDiaMolecule object

        Parameters
        ----------
        molecule
            molecule diagram molecule object

        """

        self.name = molecule.name

        self.fragment1 = Empty()
        self.fragment1.name = molecule.fragment1.name
        self.fragment1.e = molecule.fragment1.e
        self.fragment1.nr = molecule.fragment1.nr
        self.fragment1.atomic_number = molecule.fragment1.atomic_number
        self.fragment1.configuration = molecule.fragment1.configuration

        self.fragment2 = Empty()
        self.fragment2.name = molecule.fragment2.name
        self.fragment2.e = molecule.fragment2.e
        self.fragment2.nr = molecule.fragment2.nr
        self.fragment2.atomic_number = molecule.fragment2.atomic_number
        self.fragment2.configuration = molecule.fragment2.configuration

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