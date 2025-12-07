# add a reference to load the PyMOdia library
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pymodia import PyMoDia, Atom, Molecule, subscript
from pyqint import MoleculeBuilder, HF
import numpy as np

# PyQInt calculations
mol = MoleculeBuilder().from_name('ch4')
pyqint_result = HF().rhf(mol, 'sto3g')

# Rounding PyQInt results for PyMoDia
mo_energies = np.round(pyqint_result['orbe'], 3)
orbc = np.round(pyqint_result['orbc'], 3)

# Keeping original energy levels for energy bar
energies = mo_energies.copy()

# Increase distance of 1pi* and 2sigma for readability diagram
mo_energies[5] = 0.1
mo_energies[6] = mo_energies[5]
mo_energies[7] = mo_energies[5]

# Setting up PyMoDia objects
C = Atom("C")
H = Atom("H")
mol_name = subscript("CH4")
CH4 = Molecule(mol_name, C, 1, H, 4)

# Making diagram
diagram = PyMoDia(CH4, mo_energies, orbc, level_width=70, main_color='#000000')
diagram.draw_levels(colors_mo=['#000000'], colors_ao1=['#000000'], colors_ao2=['#000000'])
diagram.draw_occupancies(color='#DD0000')
diagram.draw_contributions(abs_cutoff=0.3, print_coeff=True, color='#555555')
diagram.draw_energy_scale(labels=energies)
diagram.draw_labels(['1a1', '2a1', '1t2', '1t2', '1t2',
                     '2t2', '2t2', '2t2', '3a1'], 'mo_ao')

# Save image
diagram.image.save_svg("mo_diagram_ch4.svg")