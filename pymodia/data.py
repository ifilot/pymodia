from . import MoDiaMolecule
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
            self.set_molecule(kwargs['molecule'])

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

    def set_molecule(self, molecule):
        """
        Set the molecule data based on a MoDiaMolecule object

        Parameters
        ----------
        molecule
            molecule diagram molecule object

        """

        self.name = molecule.name

        self.atom1 = Empty()
        self.atom1.name = molecule.atom1.name
        self.atom1.e = molecule.atom1.e
        self.atom1.nr = molecule.atom1.nr
        self.atom1.atomic_number = molecule.atom1.atomic_number
        self.atom1.configuration = molecule.atom1.configuration

        self.atom2 = Empty()
        self.atom2.name = molecule.atom2.name
        self.atom2.e = molecule.atom2.e
        self.atom2.nr = molecule.atom2.nr
        self.atom2.atomic_number = molecule.atom2.atomic_number
        self.atom2.configuration = molecule.atom2.configuration

        return self

    def from_pyqint(self, results):

        self.moe = results['orbe']
        self.orbc = results['orbc']

        diag = np.diagonal(results['fock']).tolist()

        nr_a1 = self.atom1.nr

        level_a_1 = self.__nr_levels(self.atom1.atomic_number)
        level_a_2 = self.__nr_levels(self.atom1.atomic_number)

        self.atom1.e = diag[0:level_a_1]

        if nr_a1 == 1:
            self.atom2.e = diag[level_a_1:level_a_1+level_a_2+1]
        else:
            self.atom2.e = diag[nr_a1*level_a_1:nr_a1*level_a_1+level_a_2+1]

        return self

    def __nr_levels(self, atomic_number):

        if atomic_number <= 2:
            return 1
        elif atomic_number <= 4:
            return 2
        elif atomic_number <= 10:
            return 5
        elif atomic_number <= 12:
            return 6
        elif atomic_number <= 18:
            return 9
        else:
            raise Exception("Higher atomic numbers not yet supported")

    def from_json(self, json):
        """
        Reads json file and import data

        Parameters
        ----------
        json
            file path to json file with data

        """

    def save_json(self, path):
        """
        Saves data from MoDiaData object to json file

        Parameters
        ----------
        path
            path to save json file to

        """
