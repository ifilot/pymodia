import os
from pymodia import MoDia, MoDiaData, autobuild_from_pyqint, MoDiaSettings
from pyqint import MoleculeBuilder, HF, FosterBoys
import numpy as np
import json

# Perform PyQInt calculations for CO and its localization
mol = MoleculeBuilder().from_name('co')
res = HF().rhf(mol, 'sto3g')

# adjust settings
settings = MoDiaSettings()
settings.orbc_color = '#555555'
settings.arrow_color = '#CC0000'

# attempt to automatically create mol and fragments from calculation
mol, f1, f2 = autobuild_from_pyqint(res, name='co')

# we make here a small adjustment to the height of the 5σ orbital to avoid
# overlap with the 2x2π MO
moe = res['orbe']
moe[6] += 0.1

# build data object
data = MoDiaData(mol, f1, f2)
data.set_moe(moe)

diagram = MoDia(data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=['1σ', '2σ', '3σ', '4σ', '1π', '1π', '5σ', '2π', '2π', '6σ'],
                settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_co_canonical.svg"))

# making diagram for localized orbitals
resfb = FosterBoys(res).run()
resfb['nuclei'] = res['nuclei'] # no longer required from PyQInt >= 1.2.0
mol, f1, f2 = autobuild_from_pyqint(resfb, name='co')

# we make here a small adjustment to the height of the third orbital to avoid
# overlap with the triple degenerate state of the localized MOs of CO
moe = resfb['orbe']
moe[2] -= 0.5
moe[6] += 0.1

# build data object
data = MoDiaData(mol, f1, f2)
data.set_moe(moe)

# construct diagram
labels = [''] * len(resfb['orbe'])
diagram = MoDia(data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=labels,
                settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_co_localized.svg"))