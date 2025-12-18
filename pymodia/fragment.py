import os
import json
from . import superscript


class MoDiaFragment():
    """
    Creates atom instances to plug into the molecule class
    """

    def __init__(self, labels, energy_levels):

        self.labels = labels
        self.energies = energy_levels
