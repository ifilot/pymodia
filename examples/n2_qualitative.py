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
orbe = [-15.1, -14.9, -1.2, -0.8, 0.1, 0.5, 0.5, 1.5, 1.5, 2]
orbc = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]]
ao_e = [-15, -1, 1, 1, 1]

# Setting up PyMoDia objects
mol_name = subscript("N2")
mol = MoDiaMolecule(mol_name, orbe, orbc, 14)
n1 = MoDiaFragment('N', ao_e, 7, {i:i for i in range(5)})
n2 = MoDiaFragment('N', ao_e, 7, {i+5:i for i in range(5)})
data = MoDiaData(mol, n1, n2)

mo_colors = ["#000000", "#000000", "#1260CC", "#1260CC", "#1260CC",
             "#FE6E00", "#FE6E00", "#FE6E00", "#FE6E00", "#1260CC",
             "#1260CC"]
ao_colors = ["#000000", "#1260CC", "#FE6E00", "#FE6E00", "#FE6E00"]
mo_labels = ['1s', '1s', '1σ', '1σ*', '2σ', '1π', '1π', '1π*', '1π*', '2σ*']

diagram = MoDia(data, orbc_cutoff=0.9, mo_color=mo_colors, ao1_color=ao_colors,
                ao2_color=ao_colors, draw_energy_labels=False,
                mo_labels=mo_labels, draw_level_labels=True,
                level_labels_style='mo_ao')

# Save image
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_n2_qualitative.svg"))
