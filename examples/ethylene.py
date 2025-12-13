import os
from pymodia import MoDia, MoDiaData, Atom, MoDiaMolecule, subscript, MoDiaSettings
from pyqint import MoleculeBuilder, HF, FosterBoys

# Perform PyQInt calculations for CO and its localization
mol = MoleculeBuilder().from_name('ethylene')
res = HF().rhf(mol, 'sto3g')
resfb = FosterBoys(res).run()

# Setting up MoDia objects
C = Atom("C")
H = Atom("H")
mol_name = subscript("ethylene")
mol = MoDiaMolecule(mol_name, C, 2, H, 4)

# adjust settings
settings = MoDiaSettings()
settings.orbc_color = '#555555'
settings.arrow_color = '#CC0000'
settings.ao_round = 2
settings.orbc_cutoff = 0.35

# making diagram for canonical orbitals
moe = res['orbe']
print(moe)
co_data = MoDiaData(molecule=mol, moe=moe, orbc=res['orbc'])
# we make here a small adjustment to avoid overlap in the diagram
moe[4] -= 0.05
moe[6] += 0.1
moe[7] += 0.1
moe[11] += 0.1
co_data.set_moe(moe)
labels = [''] * len(res['orbe'])
diagram = MoDia(co_data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=labels,
                settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_ethylene_canonical.svg"))

# making diagram for localized orbitals
moe = resfb['orbe']
co_data = MoDiaData(molecule=mol, moe=moe, orbc=resfb['orbc'])
# we make here a small adjustment to avoid overlap in the diagram
moe[6] += 0.1
moe[7] += 0.1
moe[11] += 0.1
co_data.set_moe(moe)
diagram = MoDia(co_data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=[[]] * len(resfb['orbe']), settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_ethylene_localized.svg"))