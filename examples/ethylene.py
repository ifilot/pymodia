"""
This script generates molecular orbital (MO) energy-level diagrams for
ethylene based on a Hartree-Fock (HF) calculation performed with PyQInt.

Two MO diagrams are produced:
  1. Canonical HF molecular orbitals.
  2. Foster-Boys localized molecular orbitals derived from the HF solution.

The workflow is:
  - Perform an RHF calculation for ethylene using a STO-3G basis.
  - Automatically construct MoDia molecule and fragment objects from the
    PyQInt results.
  - Slightly adjust selected orbital energies to avoid visual overlap in the
    rendered diagram.
  - Generate and export SVG MO diagrams using MoDia for both canonical and
    localized orbitals.

The resulting diagrams visualize the correspondence between atomic orbitals
and molecular orbitals for ethylene in both representations.
"""

import os
from pymodia import MoDia, MoDiaData, MoDiaSettings, autobuild_from_pyqint
from pyqint import MoleculeBuilder, HF, FosterBoys

# Perform PyQInt calculations for CO and its localization
mol = MoleculeBuilder().from_name('ethylene')
res = HF().rhf(mol, 'sto3g')

# adjust settings
settings = MoDiaSettings()
settings.orbc_color = '#555555'
settings.arrow_color = '#CC0000'
settings.ao_round = 2
settings.mo_round = 2
settings.orbc_cutoff = 0.4

# attempt to automatically create mol and fragments from calculation
mol, f1, f2 = autobuild_from_pyqint(res, name='ethylene')

# we make here a small adjustment to avoid overlapping states in the diagram
moe = res['orbe']
moe[4] -= 0.05
moe[6] += 0.1
moe[7] += 0.1
moe[11] += 0.1

# build data object
data = MoDiaData(mol, f1, f2)
data.set_moe(moe)

labels = [''] * len(res['orbe'])

# construct diagram
diagram = MoDia(data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=labels,
                settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_ethylene_canonical.svg"))

# making diagram for localized orbitals
resfb = FosterBoys(res).run()
resfb['nuclei'] = res['nuclei'] # no longer required from PyQInt >= 1.2.0
mol, f1, f2 = autobuild_from_pyqint(resfb, name='ethylene')

# build data object
data = MoDiaData(mol, f1, f2)
moe = resfb['orbe']
moe[6] += 0.1
moe[7] += 0.1
data.set_moe(moe)

# construct diagram
diagram = MoDia(data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=labels,
                settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_ethylene_localized.svg"))