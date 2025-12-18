import os
from pymodia import MoDia, MoDiaData, Atom, MoDiaMolecule, MoDiaFragment, subscript, MoDiaSettings
from pyqint import MoleculeBuilder, HF, FosterBoys
import json

with open('../pymodia/atom_data.json') as f:
    data = json.load(f)
ao_c = data['C']['ao_energy']
ao_h = data['H']['ao_energy']

# Perform PyQInt calculations for CO and its localization
mol = MoleculeBuilder().from_name('ethylene')
res = HF().rhf(mol, 'sto3g')
resfb = FosterBoys(res).run()

c_mapping = {i: i for i in range(5)}
c_mapping.update({i: i - 7 for i in range(7, 12)})
h_mapping = {i: 0 for i in [6,7,12,13]}

# Setting up MoDia objects
c = MoDiaFragment("2xC", ao_c, 6, c_mapping, sublabel='1s 2s 2p')
h = MoDiaFragment("4xH", ao_h, 1, h_mapping, sublabel='1s')
mol_name = subscript("ethylene")
mol = MoDiaMolecule(mol_name, res['orbe'], res['orbc'], res['nelec'])

# adjust settings
settings = MoDiaSettings()
settings.orbc_color = '#555555'
settings.arrow_color = '#CC0000'
settings.ao_round = 2
settings.orbc_cutoff = 0.1

# making diagram for canonical orbitals
moe = res['orbe']
data = MoDiaData(mol, c, h)
# we make here a small adjustment to avoid overlap in the diagram
moe[4] -= 0.05
moe[6] += 0.1
moe[7] += 0.1
moe[11] += 0.1
data.set_moe(moe)
labels = [''] * len(res['orbe'])
diagram = MoDia(data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=labels,
                settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_ethylene_canonical.svg"))

# # making diagram for localized orbitals
# moe = resfb['orbe']
# co_data = MoDiaData(molecule=mol, moe=moe, orbc=resfb['orbc'])
# # we make here a small adjustment to avoid overlap in the diagram
# moe[6] += 0.1
# moe[7] += 0.1
# moe[11] += 0.1
# co_data.set_moe(moe)
# diagram = MoDia(co_data, draw_level_labels=True, level_labels_style='mo_ao',
#                 mo_labels=[[]] * len(resfb['orbe']), settings=settings)
# diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_ethylene_localized.svg"))