from pymodia import MoDia, MoDiaData, MoDiaMolecule, Atom, subscript
import pyqint
import os
import sys
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# PyQInt calculations
mol = pyqint.MoleculeBuilder().from_name('ethylene')

cgfs, atoms = mol.build_basis('sto3g')
res = pyqint.HF().rhf(mol, basis='sto3g')
resfb = pyqint.FosterBoys(res).run()

# Setting up PyMoDia objects
diag = np.diagonal(res['fock']).tolist()
e = [-11.02, -1.54, -0.27, -0.27, -0.27]
C = Atom("C", e)
H = Atom("H", [-0.46])
molname = subscript("Ethylene")
Mol = MoDiaMolecule(molname, C, 2, H, 4)


ao1 = ['#000000']
ao2 = ['#785EF0']
mo_canonical = ['#000000']
mo_local = ['#000000']

# Canonical diagram
C2H4_canonical = MoDiaData(molecule=Mol, moe=res['orbe'], orbc=res['orbc'])
canonical = MoDia(C2H4_canonical)

# localized diagram
C2H4_local = MoDiaData(molecule=Mol, moe=resfb['orbe'], orbc=resfb['orbc'])
local = MoDia(C2H4_local, draw_level_labels=True, level_labels_style='mo_ao',
              mo_labels=['1s', '1s', 'C-H', 'C-H', 'C-H', 'C-H',
                         'double bond', 'double bond', '', '', '', '', '', '', '', '', '', ''])

# Save images
canonical.export_svg(os.path.join(
    os.path.dirname(__file__), "Ethylene_canonical.svg"))
local.export_svg(os.path.join(
    os.path.dirname(__file__), "Ethylene_localized.svg"))
