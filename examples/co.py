# add a reference to load the PyMOdia library
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pymodia import MoDia, MoDiaData, Atom, MoDiaMolecule, subscript, MoDiaSettings
from pyqint import MoleculeBuilder, HF, FosterBoys
import numpy as np

# PyQInt calculations
mol = MoleculeBuilder().from_name('co')
res = HF().rhf(mol, 'sto3g')
resfb = FosterBoys(res).run()

# Rounding PyQInt results for MoDia
mo_energies = np.round(res['orbe'], 3)
orbc = np.round(res['orbc'], 3)

# Keeping original energy levels for energy bar
energies = mo_energies.copy()

# # Increase distance of 5sigma
mo_energies[3] -= 0.1
mo_energies[6] += 0.2

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
co_data = MoDiaData(molecule=mol, moe=res['orbe'], orbc=res['orbc'])
diagram = MoDia(co_data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=['1σ', '2σ', '3σ', '4σ', '1π','1π', '5σ', '2π', '2π', '6σ'],
                settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_co_canonical.svg"))

# making diagram for localized orbitals
co_data = MoDiaData(molecule=mol, moe=resfb['orbe'], orbc=resfb['orbc'])
diagram = MoDia(co_data, draw_level_labels=True, level_labels_style='mo_ao',
                mo_labels=[[]] * len(resfb['orbe']), settings=settings)
diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_co_localized.svg"))