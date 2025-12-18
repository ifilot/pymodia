import os
import sys

# MO data
mo_energies = [-0.58, 0.67]
orbc = [[-0.55, -0.55], [1.21, -1.21]]

#
# Setting up PyMoDia objects
#

# build fragment from name and levels
h = MoDiaFragment("H", [-0.08])

# build molecule name
mol_name = subscript("H2")

# build molecule and specify fragments
mol = MoDiaMolecule(mol_name, mo_energies, orbc)

# build diagram
h2 = MoDiaData(mol, h, h)

diagram = MoDia(h2, outer_height=200, core_height=20, height=320,
                mo_color=['#1aa7ec', '#1aa7ec'], draw_orbc=True,
                mo_labels=['σ', 'σ*'], draw_level_labels=True,
                level_labels_style='mo')

# Save image
diagram.export_svg(os.path.join(
    os.path.dirname(__file__), "H2_mo_diagram.svg"))
