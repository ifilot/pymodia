import os
import json
from . import superscript


class MoDiaFragment():
    """
    Creates atom instances to plug into the molecule class
    """

    def __init__(self, name, state_energies, nelec, bf_mapping, sublabel = None):
        self.state_energies = state_energies
        self.nelec = nelec
        self.name = name
        self.sublabel = sublabel
        self.atomic_number = 1
        self.bf_mapping = bf_mapping