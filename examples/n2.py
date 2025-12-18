"""
This script generates a molecular orbital (MO) diagram for the nitrogen
molecule (N₂) based on an ab initio Hartree–Fock calculation performed with
PyQInt.

The workflow is:
  - Define the N₂ molecular geometry at a fixed internuclear separation.
  - Perform a geometry optimization and retrieve the resulting electronic
    structure data using a STO-3G basis.
  - Automatically construct MoDia molecule and fragment objects from the
    PyQInt results.
  - Customize diagram appearance using MoDia settings.
  - Generate and export an SVG molecular orbital diagram using MoDia.

The resulting diagram visualizes the canonical Hartree–Fock molecular orbitals
of N₂, showing the energetic ordering and atomic-orbital contributions.
"""

import os
from pymodia import MoDia, MoDiaData, autobuild_from_pyqint, MoDiaSettings, subscript
from pyqint import GeometryOptimization, FosterBoys, Molecule

# Perform PyQInt calculations for N2
dist = 0.5669
mol = Molecule('N2')
mol.add_atom('N', 0.0, 0.0, -dist, unit='angstrom')
mol.add_atom('N', 0.0, 0.0, dist, unit='angstrom')
res = GeometryOptimization().run(mol, 'sto3g')['data']

# adjust settings
settings = MoDiaSettings()
settings.orbc_color = '#555555'
settings.arrow_color = '#CC0000'

# attempt to automatically create mol and fragments from calculation
mol, f1, f2 = autobuild_from_pyqint(res, name=subscript('N2'))

# build data object
data = MoDiaData(mol, f1, f2)
diagram = MoDia(data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=[''] * len(res['orbe']),
                settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_n2_canonical.svg"))