<<<<<<< HEAD
from pymodia import MoDia, MoDiaData, MoDiaMolecule, Atom, subscript
import pyqint
import os
import sys
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


# PyQInt calculations
mol = pyqint.Molecule()
dist = 1.78/2

mol.add_atom('C', 0.0, 0.0, 0.0, unit='angstrom')
mol.add_atom('H', dist, dist, dist, unit='angstrom')
mol.add_atom('H', -dist, -dist, dist, unit='angstrom')
mol.add_atom('H', -dist, dist, -dist, unit='angstrom')
mol.add_atom('H', dist, -dist, -dist, unit='angstrom')

cgfs, atoms = mol.build_basis('sto3g')
res = pyqint.HF().rhf(mol, basis='sto3g')

# Setting up PyMoDia objects
diag = np.diagonal(res['fock']).tolist()
C = Atom("C", diag[0:5])
H = Atom("H", [diag[5]])
molname = subscript("CH4")
Mol = MoDiaMolecule(molname, C, 1, H, 4)

CH4 = MoDiaData(molecule=Mol, moe=res['orbe'], orbc=res['orbc'])

ao1_c = ['#000000', '#785EF0', '#fe6100', '#fe6100', '#fe6100']
ao2_c = ['#785EF0']
mo_c = ['#000000', '#785EF0', '#fe6100', '#fe6100', '#fe6100', '#785EF0',
        '#fe6100', '#fe6100', '#fe6100']
diagram = MoDia(CH4, ao1_color=ao1_c, ao2_color=ao2_c, mo_color=mo_c,
                draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=['1s', '1σ', '1π', '1π', '1π',
                           '1σ*', '1π*', '1π*', '1π*'])

# Save image
diagram.export_svg(os.path.join(
    os.path.dirname(__file__), "CH4_mo_diagram.svg"))
=======
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
>>>>>>> e8f353ff8c536f70cdfe6b5933f454f01b163c18
