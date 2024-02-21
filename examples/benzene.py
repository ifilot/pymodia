from pymodia import MoDia, MoDiaData, MoDiaMolecule, Atom, subscript
import pyqint
import os
import sys
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


# PyQInt calculations
# mol = pyqint.MoleculeBuilder().from_name('benzene')
# res = pyqint.HF().rhf(mol, basis='sto3g')

# print(res['orbe'])

# # Setting up PyMoDia objects
# diag = np.diagonal(res['fock']).tolist()
# C = Atom("C", [-11.065219467466152, -1.3906818459015957, -0.07200908036358822, -0.07200908036371789, -0.07200908036366016])
# H = Atom("H", [diag[-1]])
# molname = subscript("Benzene")
# Mol = MoDiaMolecule(molname, C, 6, H, 6)

benzene = MoDiaData(
    molecule=Mol, moe=res['orbe'], orbc=res['orbc'])

diagram = MoDia(benzene, mo_round=1, core_cutoff=-10)

# Save image
diagram.export_svg(os.path.join(
    os.path.dirname(__file__), "benzene_mo_diagram.svg"))
