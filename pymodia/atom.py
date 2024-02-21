import os
import json
from . import superscript


class Atom():
    """
    Creates atom instances to plug into the molecule class
    """

    def __init__(self, atomic_symbol, energy_levels=None):

        ao_dict_file = open(os.path.join(os.path.dirname(__file__),
                                         'atom_data.json'), "r")
        ao_dict = json.load(ao_dict_file)
        ao_dict_file.close()

        self.name = atomic_symbol

        ai = ao_dict[self.name]

        if energy_levels is None:
            self.energies = ai["ao_energy"]
        else:
            self.energies = energy_levels

        self.full_name = ai["atom"]
        self.atomic_number = ai["atomic_number"]
        self.labels = ai["labels"]
        self.configuration = superscript(ai["configuration"])
