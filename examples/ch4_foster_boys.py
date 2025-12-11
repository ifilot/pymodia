from pymodia import MoDia, MoDiaData, MoDiaMolecule, Atom, subscript
import pyqint
import os
import sys
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# PyQInt calculations
mol = pyqint.MoleculeBuilder().from_name('ch4')

cgfs, atoms = mol.build_basis('sto3g')
res = pyqint.HF().rhf(mol, basis='sto3g')
resfb = pyqint.FosterBoys(res).run()

# Setting up PyMoDia objects
diag = np.diagonal(res['fock']).tolist()
C = Atom("C", diag[0:5])
H = Atom("H", [diag[5]])
molname = subscript("CH4")
Mol = MoDiaMolecule(molname, C, 1, H, 4)


ao1 = ['#000000', '#785EF0', '#fe6100', '#fe6100', '#fe6100']
ao2 = ['#785EF0']
mo_canonical = ['#000000', '#785EF0', '#fe6100', '#fe6100', '#fe6100', '#000000',
                '#000000', '#000000', '#000000']
mo_local = ['#000000', '#785EF0', '#785EF0', '#785EF0', '#785EF0', '#000000',
            '#000000', '#000000', '#000000']

# Canonical diagram
CH4_canonical = MoDiaData(molecule=Mol, moe=res['orbe'], orbc=res['orbc'])
canonical = MoDia(CH4_canonical, ao1_color=ao1, ao2_color=ao2, mo_color=mo_canonical,
                  draw_level_labels=True, level_labels_style='mo_ao',
                  mo_labels=['1s', '1a1', '1t2', '1t2', '1t2', '',
                             '', '', ''])
# localized diagram
CH4_local = MoDiaData(molecule=Mol, moe=resfb['orbe'], orbc=resfb['orbc'])
local = MoDia(CH4_local, ao1_color=ao1, ao2_color=ao2, mo_color=mo_local,
              draw_level_labels=True, level_labels_style='mo_ao',
              mo_labels=['1s', 'σ', 'σ', 'σ', 'σ', '', '', '', ''])

# Save images
canonical.export_svg(os.path.join(
    os.path.dirname(__file__), "CH4_canonical.svg"))
local.export_svg(os.path.join(
    os.path.dirname(__file__), "CH4_localized.svg"))
