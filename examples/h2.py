import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pymodia import MoDia, MoDiaData, MoDiaMolecule, Atom, subscript

# MO data
mo_energies = [-0.58, 0.67]
orbc = [[-0.55, -0.55], [1.21, -1.21]]

# Setting up PyMoDia objects
H = Atom("H", [-0.08])
Mol_name = subscript("H2")
Mol = MoDiaMolecule(Mol_name, H, 1, H, 1)

H2 = MoDiaData(molecule=Mol, moe=mo_energies, orbc=orbc)

diagram = MoDia(H2, outer_height=200, core_height=20, height=320,
                mo_color=['#1aa7ec', '#1aa7ec'], draw_orbc=True,
                mo_labels=['σ', 'σ*'], draw_level_labels=True,
                level_labels_style='mo')

# Save image
diagram.export_svg(os.path.join(
    os.path.dirname(__file__), "H2_mo_diagram.svg"))
