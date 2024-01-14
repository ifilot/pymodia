import pyqint
from pymodia import MoDia, MoDiaData, MoDiaMolecule, Atom, subscript
import sys
import os
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

diagram = MoDia(CH4)
print(diagram.data.atom2.e)

# Save image
diagram.export_svg(os.path.join(
    os.path.dirname(__file__), "CH4_mo_diagram.svg"))
