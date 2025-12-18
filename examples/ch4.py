import os
from pymodia import MoDia, MoDiaData, autobuild_from_pyqint, subscript, MoDiaSettings
from pyqint import MoleculeBuilder, HF, FosterBoys

# Perform PyQInt calculations for CO and its localization
mol = MoleculeBuilder().from_name('ch4')
res = HF().rhf(mol, 'sto3g')

# attempt to automatically create mol and fragments from calculation
mol, f1, f2 = autobuild_from_pyqint(res, name=subscript('CH4'))

# adjust settings
settings = MoDiaSettings()
settings.orbc_color = '#555555'
settings.arrow_color = '#000000'
settings.mo_color = ['#000000'] * len(res['orbc'])
settings.mo_color[1] = '#f58742'
settings.mo_color[2:8] = ['#5e2ca3'] * 6
settings.mo_color[8] = '#f58742'
settings.ao1_color = ['#000000', '#f58742', '#5e2ca3', '#5e2ca3', '#5e2ca3']
settings.ao2_color = ['#f58742']

# making diagram for canonical orbitals
data = MoDiaData(mol, f1, f2)
diagram = MoDia(data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=['1A'+subscript('1'), 
                           '2A'+subscript('1'),
                           '1T'+subscript('2'), 
                           '1T'+subscript('2'), 
                           '1T'+subscript('2'), '', '', '', '', ''],
                settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_ch4_canonical.svg"))

# adjust settings for localized orbitals
settings = MoDiaSettings()
settings.orbc_color = '#555555'
settings.arrow_color = '#000000'
settings.mo_color = ['#000000'] * len(res['orbc'])
settings.mo_color[1:5] = ['#f022ca'] * 4
settings.ao1_color = ['#000000', '#f58742', '#5e2ca3', '#5e2ca3', '#5e2ca3']
settings.ao2_color = ['#f58742']

# making diagram for localized orbitals
resfb = FosterBoys(res).run()
resfb['nuclei'] = res['nuclei'] # no longer required from PyQInt >= 1.2.0
mol, f1, f2 = autobuild_from_pyqint(resfb, name=subscript('CH4'))
data = MoDiaData(mol, f1, f2)
diagram = MoDia(data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=[[]] * len(resfb['orbe']), settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_ch4_localized.svg"))