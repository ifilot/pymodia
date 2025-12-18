from typing import List, Iterable
import numpy as np

class MoDiaMolecule:
    """
    Container for molecular information required to construct a MoDia
    molecular orbital (MO) diagram.

    This class stores molecular orbital energies, coefficients, and the
    total number of electrons associated with the molecule.
    """

    def __init__(
        self,
        name: str,
        state_energies: Iterable[float],
        state_coefficients: np.ndarray,
        nelec: int,
    ) -> None:
        """
        Initialize a molecule.

        Parameters
        ----------
        name
            Name of the molecule.
        state_energies
            Energies of the molecular orbitals.
        state_coefficients
            Molecular orbital coefficient matrix.
        nelec
            Total number of electrons in the molecule.
        """
        self.name: str = name
        self.state_energies: List[float] = state_energies
        self.state_coefficients: np.ndarray = state_coefficients
        self.nelec: int = nelec
