import os
from pymodia import MoDia, MoDiaData, Atom, MoDiaMolecule, subscript, MoDiaSettings
from pyqint import MoleculeBuilder, HF, FosterBoys

# Perform PyQInt calculations for CO and its localization
mol = MoleculeBuilder().from_name('co')
res = HF().rhf(mol, 'sto3g')
resfb = FosterBoys(res).run()

# Setting up MoDia objects
C = Atom("C")
O = Atom("O")
mol_name = subscript("CO")
mol = MoDiaMolecule(mol_name, O, 1, C, 1)

# adjust settings
settings = MoDiaSettings()
settings.orbc_color = '#555555'
settings.arrow_color = '#CC0000'

# making diagram for canonical orbitals
moe = res['orbe']
co_data = MoDiaData(molecule=mol, moe=moe, orbc=res['orbc'])
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
co_data = MoDiaData(molecule=mol, moe=moe, orbc=resfb['orbc'])
# we make here a small adjustment to the height of the third orbital to avoid
# overlap with the triple degenerate state of the localized MOs of CO
moe[2] -= 0.1
co_data.set_moe(moe)
diagram = MoDia(co_data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=[[]] * len(resfb['orbe']), settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_co_localized.svg"))