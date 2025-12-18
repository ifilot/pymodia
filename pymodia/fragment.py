from typing import Dict, Optional, Iterable

class MoDiaFragment():
    """
    Creates atom instances to plug into the molecule class
    """
    def __init__(
        self,
        name: str,
        state_energies: Iterable[float],
        nelec: int,
        bf_mapping: Dict[int, int],
        sublabel: Optional[str] = None,
    ) -> None:
        """
        Initialize a fragment.

        Parameters
        ----------
        name
            Name of the fragment.
        state_energies
            Energies of the fragment-local states.
        nelec
            Number of electrons associated with the fragment.
        bf_mapping
            Mapping from global basis-function indices to fragment-local
            indices.
        sublabel
            Optional sublabel used for display or grouping.
        """
        self.state_energies = state_energies
        self.nelec = nelec
        self.name = name
        self.sublabel = sublabel
        self.atomic_number = 1
        self.bf_mapping = bf_mapping