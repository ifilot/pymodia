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