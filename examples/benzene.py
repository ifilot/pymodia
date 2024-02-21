from pymodia import MoDia, MoDiaData, MoDiaMolecule, Atom, subscript
import pyqint
import os
import sys
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# PyQInt calculations
mol = pyqint.MoleculeBuilder().from_name('benzene')
res = pyqint.HF().rhf(mol, basis='sto3g')

# Setting up PyMoDia objects
C = Atom("C", [-11.065, -1.391, -0.072, -0.072, -0.072])
H = Atom("H", [-0.214])
molname = subscript("Benzene")
Mol = MoDiaMolecule(molname, C, 6, H, 6)

benzene = MoDiaData(
    molecule=Mol, moe=res['orbe'], orbc=res['orbc'])

diagram = MoDia(benzene, height=800, outer_height=600, level_width=80)

# Save image
diagram.export_svg(os.path.join(
    os.path.dirname(__file__), "benzene_mo_diagram.svg"))
