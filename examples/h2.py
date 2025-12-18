"""
This script generates a molecular orbital (MO) diagram for the hydrogen
molecule (H₂) based on a Hartree–Fock (HF) calculation performed with PyQInt
using a STO-3G basis set.

The workflow is:
  - Build the H₂ molecular structure automatically.
  - Perform a restricted Hartree–Fock calculation.
  - Automatically construct MoDia molecule and fragment objects from the
    PyQInt results.
  - Generate and export an SVG molecular orbital diagram using MoDia.

The resulting diagram illustrates the formation of bonding (σ) and
antibonding (σ*) molecular orbitals from hydrogen 1s atomic orbitals and
serves as a minimal example of MO diagram construction with MoDia.
"""

import os
from pymodia import MoDia, MoDiaData, autobuild_from_pyqint, MoDiaSettings, subscript
from pyqint import MoleculeBuilder, HF

# Perform PyQInt calculations for CO and its localization
mol = MoleculeBuilder().from_name('h2')
res = HF().rhf(mol, 'sto3g')

# adjust settings
settings = MoDiaSettings()
settings.orbc_color = '#555555'
settings.arrow_color = '#CC0000'

# attempt to automatically create mol and fragments from calculation
mol, f1, f2 = autobuild_from_pyqint(res, name=subscript('H2'))

# build data object
data = MoDiaData(mol, f1, f2)

diagram = MoDia(data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=['1σ', '2σ*'],
                settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_h2.svg"))