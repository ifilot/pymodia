ao_dict = {
    'H': {
        "atom": "Hydrogen",
        "atomic_number": 1,
        "configuration": "(1s¹)",
        "labels": ["1s"],
        "ao_energy": [-0.50]
    },
    'He': {
        "atom": "Helium",
        "atomic_number": 2,
        "configuration": "(1s²)",
        "labels": ["1s"],
        "ao_energy": [-0.50]
    },
    'Li': {
        "atom": "Lithium",
        "atomic_number": 3,
        "configuration": "(1s²2s¹)",
        "labels": ["1s", "2s"],
        "ao_energy": [-0.50]
    },
    'Be': {
        "atom": "Beryllium",
        "atomic_number": 4,
        "configuration": "(1s²2s²)",
        "labels": ["1s", "2s"],
        "ao_energy": [-0.50]
    },
    'B': {
        "atom": "Boron",
        "atomic_number": 5,
        "configuration": "(1s²2s²2p¹)",
        "labels": ["1s", "2s", "2p"],
        "ao_energy": [-0.50]
    },
    'C': {
        "atom": "Carbon",
        "atomic_number": 6,
        "configuration": "(1s²2s²2p²)",
        "labels": ["1s", "2s", "2p"],
        "ao_energy": [-11.32, -0.71, -0.43, -0.43, -0.43]
    },
    'N': {
        "atom": "Nitrogen",
        "atomic_number": 7,
        "configuration": "(1s²2s²2p³)",
        "labels": ["1s", "2s", "2p"],
        "ao_energy": [-0.50]
    },
    'O': {
        "atom": "Oxygen",
        "atomic_number": 8,
        "configuration": "(1s²2s²2p⁴)",
        "labels": ["1s", "2s", "2p"],
        "ao_energy": [-20.66, -1.24, -0.60, -0.60, -0.60]
    },
    'F': {
        "atom": "Fluorine",
        "atomic_number": 9,
        "configuration": "(1s²2s²2p⁵)",
        "labels": ["1s", "2s", "2p"],
        "ao_energy": [-0.50]
    },
    'Ne': {
        "atom": "Neon",
        "atomic_number": 10,
        "configuration": "(1s²2s²2p⁶)",
        "labels": ["1s", "2s", "2p"],
        "ao_energy": [-0.50]
    },
    'Na': {
        "atom": "Sodium",
        "atomic_number": 11,
        "configuration": "([Ne]3s¹)",
        "labels": ["1s", "2s", "2p", "3s"],
        "ao_energy": [-0.50]
    },
    'Mg': {
        "atom": "Magnesium",
        "atomic_number": 12,
        "configuration": "([Ne]3s²)",
        "labels": ["1s", "2s", "2p", "3s"],
        "ao_energy": [-0.50]
    },
    'Al': {
        "atom": "Aluminium",
        "atomic_number": 13,
        "configuration": "([Ne]3s²3p¹)",
        "labels": ["1s", "2s", "2p", "3s", "3p"],
        "ao_energy": [-0.50]
    },
    'Si': {
        "atom": "Silicon",
        "atomic_number": 14,
        "configuration": "([Ne]3s²3p²)",
        "labels": ["1s", "2s", "2p", "3s", "3p"],
        "ao_energy": [-0.50]
    },
    'P': {
        "atom": "Phosphorus",
        "atomic_number": 15,
        "configuration": "([Ne]3s²3p³)",
        "labels": ["1s", "2s", "2p", "3s", "3p"],
        "ao_energy": [-0.50]
    },
    'S': {
        "atom": "Sulfur",
        "atomic_number": 16,
        "configuration": "([Ne]3s²3p⁴)",
        "labels": ["1s", "2s", "2p", "3s", "3p"],
        "ao_energy": [-0.50]
    },
    'Cl': {
        "atom": "Chlorine",
        "atomic_number": 17,
        "configuration": "([Ne]3s²3p⁵)",
        "labels": ["1s", "2s", "2p", "3s", "3p"],
        "ao_energy": [-0.50]
    },
    'Ar': {
        "atom": "Argon",
        "atomic_number": 18,
        "configuration": "([Ne]3s²3p⁶)",
        "labels": ["1s", "2s", "2p", "3s", "3p"],
        "ao_energy": [-0.50]
    },
    'K': {
        "atom": "Potassium",
        "atomic_number": 19,
        "configuration": "([Ar]4s¹)",
        "labels": ["1s", "2s", "2p", "3s", "3p", "4s"],
        "ao_energy": [-0.50]
    },
}


class Atom():
    """
    Creates atom instances to plug into the molecule class
    """

    def __init__(self, atomic_symbol, energy_levels=None):
        self.name = atomic_symbol

        ai = ao_dict[self.name]

        if energy_levels is None:
            self.energies = ai["ao_energy"]
        else:
            self.energies = energy_levels

        self.full_name = ai["atom"]
        self.atomic_number = ai["atomic_number"]
        self.labels = ai["labels"]
        self.configuration = ai["configuration"]
