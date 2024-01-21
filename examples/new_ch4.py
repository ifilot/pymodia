from pymodia import MoDia, MoDiaData, MoDiaMolecule, Atom, subscript
import pyqint
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


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

# Setting up PyMoDia objects
C = Atom("C")
H = Atom("H")
molname = subscript("CH4")
Mol = MoDiaMolecule(molname, C, 1, H, 4)

CH4 = MoDiaData(molecule=Mol).from_pyqint(res)

ao1_c = ['#000000', '#785EF0', '#fe6100', '#fe6100', '#fe6100']
ao2_c = ['#785EF0']
mo_c = ['#000000', '#785EF0', '#fe6100', '#fe6100', '#fe6100', '#785EF0',
        '#fe6100', '#fe6100', '#fe6100']
diagram = MoDia(CH4, ao1_color=ao1_c, ao2_color=ao2_c, mo_color=mo_c,
                draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=['1s', '1σ', '1π', '1π', '1π',
                           '2σ*', '2π*', '2π*', '2π*'])

# Save image
diagram.export_svg(os.path.join(
    os.path.dirname(__file__), "CH4_mo_diagram.svg"))
