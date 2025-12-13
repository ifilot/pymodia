import pyqint
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pymodia import MoDia, MoDiaData, MoDiaMolecule, Atom, subscript

# PyQInt calculations
mol = pyqint.Molecule()
dist = 0.5669

mol.add_atom('N', 0.0, -dist, 0.0, unit='angstrom')
mol.add_atom('N', 0.0, dist, 0.0, unit='angstrom')

cgfs, atoms = mol.build_basis('sto3g')
res = pyqint.HF().rhf(mol, basis='sto3g')
resfb = pyqint.FosterBoys(res).run()

# Setting up PyMoDia objects
e = [-16.5, -1, 0, 0, 0]
N = Atom("N", e)
molname = subscript("N2")
Mol = MoDiaMolecule(molname, N, 1, N, 1)

res['orbe'][1] = 1.01*res['orbe'][0]
resfb['orbe'][1] = 1.01*resfb['orbe'][0]


ao = ['#000000', '#785EF0', '#fe6100', '#fe6100', '#fe6100']
mo_canonical = ['#000000']
mo_local = ['#000000', '#000000', '#785EF0', '#785EF0', '#785EF0', '#000000',
            '#785EF0', '#785EF0', '#785EF0', '#785EF0']

# Canonical diagram
N2_canonical = MoDiaData(molecule=Mol, moe=res['orbe'], orbc=res['orbc'])
canonical = MoDia(N2_canonical, ao1_color=ao, ao2_color=ao,
                  mo_color=mo_canonical, draw_level_labels=True,
                  level_labels_style='mo_ao', mo_labels=['1σ', '1σ*',
                                                         '2σ', '2σ*',
                                                         '1π', '2π',
                                                         '1π*', '3σ',
                                                         '2π*', '3σ*'])
# localized diagram
N2_local = MoDiaData(molecule=Mol, moe=resfb['orbe'], orbc=resfb['orbc'])
local = MoDia(N2_local, ao1_color=ao, ao2_color=ao, mo_color=mo_local,
              draw_level_labels=True, level_labels_style='mo_ao',
              mo_labels=['1s', '1s',
                         'triple bond', 'triple bond', 'triple bond',
                         'lone pairs', 'lone pairs', '', '', ''])

# Save images
canonical.export_svg(os.path.join(
    os.path.dirname(__file__), "N2_canonical.svg"))
local.export_svg(os.path.join(
    os.path.dirname(__file__), "N2_localized.svg"))
