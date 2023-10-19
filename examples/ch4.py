# Note that this example works without installing PyMoDia as a system-wide
# package

import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pymodia import PyMoDia, Atom, Molecule, subscript
import pyqint
import numpy as np

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

# Rounding PyQInt results for PyMoDia
orbc = np.round(res['orbc'], 3)

# Setting up PyMoDia objects
C = Atom("C")
H = Atom("H")
molname = subscript("CH4")
Mol = Molecule(molname, C, 1, H, 4)

# Setting for the diagram
core_cutoff = -2
contribution_cutoff = 0.25

# Change canvas dimensions
outer_height = 300                      # height for the valence electrons
core_height = 80                        # height for the core electrons box
height = outer_height+core_height+150   # total height of image

# use distinct colors for core, sigma and pi orbitals in this diagram
core = "#000000"
sigma = "#1aa7ec"
pi = "#ff751f"
mo_colors = [core, core, sigma, sigma, pi, pi,
             sigma, pi, pi, sigma]

# use distinct colors for the atomic orbitals
ao_colors_carbon = [core, sigma, pi, pi, pi]
ao_colors_hydrogen = [sigma, sigma, sigma, sigma]

    # Making diagram
diagram = PyMoDia(Mol, mo_energies, orbc, outer_height=outer_height,
                  core_height=core_height, height=height,
                  core_cutoff=core_cutoff, draw_background=False)
diagram.draw_levels(colors_mo=mo_colors, 
                    colors_ao1=ao_colors_carbon,
                    colors_ao2=ao_colors_hydrogen)
diagram.draw_occupancies()
diagram.draw_contributions(contribution_cutoff)
diagram.draw_energy_scale(labels=res['orbe'])
diagram.draw_labels(['1a1', '2a1', '1t2', '1t2', '1t2',
                     '2t2', '2t2', '2t2', '3a1'], 'mo_ao')

# Save image
diagram.image.save_svg("CH4_mo_diagram.svg")