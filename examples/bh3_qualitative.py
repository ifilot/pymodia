"""
This script constructs a qualitative molecular orbital (MO) diagram for the
nitrogen molecule (N₂) using manually specified orbital energies and
coefficients.

Rather than relying on an ab initio electronic structure calculation, the
molecular orbital energies, coefficients, and atomic orbital energies are
provided explicitly to illustrate bonding, antibonding, and degenerate
orbital interactions in a pedagogical setting.

The workflow is:
  - Define approximate molecular orbital energies and coefficients.
  - Define atomic orbital energies for two nitrogen fragments.
  - Assemble MoDia molecule and fragment objects manually.
  - Customize orbital colors and labels for clarity.
  - Generate and export an SVG MO diagram using MoDia.

The resulting diagram provides a schematic, chemically intuitive
representation of the MO structure of N₂ suitable for teaching or
illustrative purposes.
"""

from pymodia import MoDia, MoDiaData, MoDiaMolecule, MoDiaFragment, subscript
import os

# MO data
orbe = [-11, -3, -2, -2, 1, 2, 2, 3]
orbc = [[1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 1, 0, 1, 1, 0],
        [0, 0, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 1, 1, 0]]

# Setting up PyMoDia objects
mol_name = subscript("BH3")
mol = MoDiaMolecule(mol_name, orbe, orbc, 8)
b = MoDiaFragment('B', [-11, -1.5, 0, 0, 1], 5, {i:i for i in range(5)})
h = MoDiaFragment('H', [-2,0,0], 3, {i+5:i for i in range(3)}, '3x1s')
data = MoDiaData(mol, b, h)

mo_colors = ["#000000", "#1260CC", "#FE6E00", "#FE6E00", "#FE00D4",
             "#FE6E00", "#FE6E00", "#1260CC"]
ao_colors1 = ["#000000", "#1260CC", "#FE6E00", "#FE6E00", "#FE00D4"]
ao_colors2 = ["#1260CC", "#FE6E00", "#FE6E00"]
mo_labels = ['A1\'(1)', 'A1\'(2)', 'E\'(1)', 'E\'(1)', 'A2\'\'(1)', 'E\'(2)*', 'E\'(2)*', 'A1\'(3)*']
ao1_labels = ['A1\' - 1s', 'A1\' - 2s', 'E\'(1) - 2px+2py', 'E\'(1) - 2px+2py', 'A2\'\' - 2pz']
ao2_labels = ['A1\'', 'E\'', 'E\'']

diagram = MoDia(data, orbc_cutoff=0.9, mo_color=mo_colors, ao1_color=ao_colors1,
                ao2_color=ao_colors2, draw_energy_labels=False,
                mo_labels=mo_labels, draw_level_labels=True,
                level_labels_style='mo_ao', ao1_labels=ao1_labels,
                ao2_labels=ao2_labels)

# Save image
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_bh3_qualitative.svg"))
