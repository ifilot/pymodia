import os
from pymodia import MoDia, MoDiaData, MoDiaFragment, MoDiaMolecule, subscript, MoDiaSettings
from pyqint import MoleculeBuilder, HF, FosterBoys
import numpy as np
import json

with open('../pymodia/atom_data.json') as f:
    data = json.load(f)
ao_c = data['C']['ao_energy']
ao_o = data['O']['ao_energy']

# Perform PyQInt calculations for CO and its localization
mol = MoleculeBuilder().from_name('co')
res = HF().rhf(mol, 'sto3g')
resfb = FosterBoys(res).run()

# Setting up MoDia objects
c = MoDiaFragment("C", ao_c, 6, sublabel='1s 2s 2p')
o = MoDiaFragment("O", ao_o, 8, sublabel='1s 2s 2p')
mol_name = subscript("CO")
mol = MoDiaMolecule(mol_name, res['orbe'], res['orbc'], res['nelec'])

# adjust settings
settings = MoDiaSettings()
settings.orbc_color = '#555555'
settings.arrow_color = '#CC0000'

# making diagram for canonical orbitals
moe = res['orbe']
co_data = MoDiaData(mol, c, o)
# we make here a small adjustment to the height of the 5σ orbital to avoid
# overlap with the 2x2π MO
moe[6] += 0.1
co_data.set_moe(moe)
diagram = MoDia(co_data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=['1σ', '2σ', '3σ', '4σ', '1π', '1π', '5σ', '2π', '2π', '6σ'],
                settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_co_canonical.svg"))

# making diagram for localized orbitals
moe = resfb['orbe']
mol = MoDiaMolecule(mol_name, resfb['orbe'], resfb['orbc'], res['nelec'])
co_data = MoDiaData(mol, c, o)
# we make here a small adjustment to the height of the third orbital to avoid
# overlap with the triple degenerate state of the localized MOs of CO
moe[2] -= 0.5
moe[6] += 0.1
co_data.set_moe(moe)
diagram = MoDia(co_data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=[[]] * len(resfb['orbe']), settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_co_localized.svg"))