import os
from pymodia import MoDia, MoDiaData, Atom, MoDiaMolecule, subscript, MoDiaSettings
from pyqint import MoleculeBuilder, HF, FosterBoys

# Perform PyQInt calculations for CO and its localization
mol = MoleculeBuilder().from_name('ch4')
res = HF().rhf(mol, 'sto3g')
resfb = FosterBoys(res).run()

# Setting up MoDia objects
C = Atom("C")
H = Atom("H")
mol_name = subscript("CH4")
mol = MoDiaMolecule(mol_name, C, 1, H, 4)

# adjust settings
settings = MoDiaSettings()
settings.orbc_color = '#555555'
settings.arrow_color = '#CC0000'
settings.ao_round = 2
settings.orbc_cutoff = 0.35
# making diagram for canonical orbitals
ch4_data = MoDiaData(molecule=mol, moe=res['orbe'], orbc=res['orbc'])
diagram = MoDia(ch4_data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=['1A'+subscript('1'), 
                           '2A'+subscript('1'),
                           '1T'+subscript('2'), 
                           '1T'+subscript('2'), 
                           '1T'+subscript('2'), '', '', '', '', ''],
                settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_ch4_canonical_default.svg"))

# adjust settings for localized orbitals
settings = MoDiaSettings()
settings.orbc_color = '#555555'
settings.arrow_color = '#CC0000'
settings.ao_round = 2
settings.orbc_cutoff = 0.35

# making diagram for localized orbitals
ch4_data = MoDiaData(molecule=mol, moe=resfb['orbe'], orbc=resfb['orbc'])
diagram = MoDia(ch4_data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=[[]] * len(resfb['orbe']), settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_ch4_localized_default.svg"))