"""
This script constructs a molecular orbital (MO) energy-level diagram for
ethylene based on a Hartree-Fock (HF) calculation performed in a
symmetry-adapted atomic orbital basis.

The workflow is as follows:
  1. Perform a restricted Hartree-Fock (RHF) calculation for ethylene using
     PyQInt and a STO-3G basis.
  2. Construct an unnormalized symmetry-adapted basis by linearly combining
     the original atomic orbitals according to ethylene's point-group
     symmetry.
  3. Reorder the symmetry-adapted basis such that orbitals belonging to the
     same irreducible representation are consecutive, yielding block-diagonal
     overlap and Fock matrices (not further used in this script)
  4. Renormalize the symmetry-adapted basis functions and recompute the HF
     solution in this new basis.
  5. Automatically partition the resulting orbitals into fragments and
     generate a molecular orbital diagram using MoDia, with orbitals grouped
     and labeled by symmetry.

The final output is an SVG molecular orbital diagram visualizing the
symmetry-adapted HF solution for ethylene.

Note:
  This script requires PyQInt >= 1.2.0.
"""

import os
from pymodia import MoDia, MoDiaData, MoDiaSettings, MoDiaFragment, MoDiaMolecule
from pyqint import MoleculeBuilder, HF, PyQInt, CGF, GTO
import numpy as np
from packaging.version import Version; 
import importlib.metadata as m;

def main():
    # Perform PyQInt calculations for CO and its localization
    res = build_symads()

    # adjust settings
    settings = MoDiaSettings()
    settings.orbc_color = '#555555'
    settings.arrow_color = '#CC0000'
    settings.mo_round = 2
    settings.ao_round = 2
    settings.orbc_cutoff = 0.3
    settings.ao1_labels = [''] * len(res['orbe']) # custom basis, do not label
    settings.ao2_labels = [''] * len(res['orbe']) # custom basis, do not label

    # attempt to automatically create mol and fragments from calculation
    ao_energies = np.diag(res['fock'])

    ao1_idx = np.array([0,1,2,4,5,6,8,9,10,12], dtype=np.int64)
    ao1_idx = ao1_idx[np.argsort([ao_energies[i] for i in ao1_idx])]
    f1 = MoDiaFragment('2xC', [ao_energies[i] for i in ao1_idx], 
                       12, {j:i for i,j in enumerate(ao1_idx)})

    ao2_idx = np.array([3,7,11,13], dtype=np.int64)
    ao2_idx = ao2_idx[np.argsort([ao_energies[i] for i in ao2_idx])]
    f2 = MoDiaFragment('4xH', [ao_energies[i] for i in ao2_idx], 
                       4, {j:i for i,j in enumerate(ao2_idx)})

    mol = MoDiaMolecule('ethylene', res['orbe'], res['orbc'], res['nelec'])

    # build data object
    data = MoDiaData(mol, f1, f2)
    labels = [''] * len(res['orbe'])

    # construct diagram
    diagram = MoDia(data, draw_level_labels=True, level_labels_style='mo_ao',
                    mo_labels=labels,
                    settings=settings)
    diagram.export_svg(os.path.join(os.path.dirname(__file__), "mo_ethylene_symads.svg"))

def build_symads():
    """
    Build symmetry-adapted basis for ethylene and use it to solve ethylene's
    electronic structure problem
    """
    # this function requires PyQInt version 1.2.0 or newer
    assert Version(m.version("pyqint")) >= Version("1.2.0")

    mol = MoleculeBuilder().from_name('ethylene')
    cgfs, nuclei = mol.build_basis('sto3g')
    res = HF().rhf(mol, 'sto3g')

    # build transformation matrix that casts the original basis onto a
    # symmetry adapted basis; no normalization is applied
    B = np.zeros((14,14))
    for i in range(0,5):
        B[i*2,i] = 1
        B[i*2,i+7] = 1
        B[i*2+1,i] = 1
        B[i*2+1,i+7] = -1

    B[10,5] = 1
    B[10,6] = 1
    B[10,-2] = 1
    B[10,-1] = 1

    B[11,5] = 1
    B[11,6] = -1
    B[11,-2] = 1
    B[11,-1] = -1

    B[12,5] = 1
    B[12,6] = 1
    B[12,-2] = -1
    B[12,-1] = -1

    B[13,5] = 1
    B[13,6] = -1
    B[13,-2] = -1
    B[13,-1] = 1

    # build yet another transformation basis that re-orders the functions such
    # that all irreps belonging to the same symmetry group are consecutive; this
    # yields block-diagonal matrices
    order = []
    overlap = B @ res['overlap'] @ B.T
    for i in range(len(overlap)):
        for j in range(len(overlap)):
            if abs(overlap[i,j]) > 0.1:
                if j not in order:
                    order.append(j)
    n = len(order)
    P = np.zeros((n, n), dtype=int)
    P[np.arange(n), order] = 1

    symfuncs = {
        'A$_{g}$'  : 4,
        'B$_{3u}$' : 4,
        'B$_{2g}$' : 1,
        'B$_{1u}$' : 1,
        'B$_{1g}$' : 2,
        'B$_{2u}$' : 2
    }
    symlabels= []
    for k,v in symfuncs.items():
        for i in range(v):
            symlabels.append(k + '(%i)' % (i+1))
    overlap = P @ overlap @ P.T

    basislabels= []
    counts = {}
    for n in nuclei:
        if n[1] not in counts.keys():
            counts[n[1]] = 1
        else:
            counts[n[1]] += 1
        
        if n[1] == 6:
            for s in ['1s', '2s', '2p_{x}', '2p_{y}', '2p_{z}']:
                basislabels.append('C$_{%s}^{(%i)}$' % (s, counts[n[1]]))
        else:
            basislabels.append('H$_{1s}^{(%i)}$' % (counts[n[1]]))

    overlap = P @ overlap @ P.T

    # construct new basis
    integrator = PyQInt()
    B = P @ B
    cgfs_symad = [CGF() for i in range(len(B))]
    for i in range(len(B)): # loop over new basis functions
        for j in range(len(cgfs)): # loop over old basis functions
            if abs(B[i,j]) > 0.01:  # verify non-negligble contribution
                for g in cgfs[j].gtos:
                    cgfs_symad[i].gtos.append(GTO(g.c*B[i,j], g.p, g.alpha, g.l, g.m, g.n))
        S = integrator.overlap(cgfs_symad[i], cgfs_symad[i])
        for g in cgfs_symad[i].gtos:
            g.c /= np.sqrt(S)

    # recalculate ethylene molecule using the new symmetry-adapted basis
    res = HF().rhf(mol, cgfs_symad)

    return res

if __name__ == '__main__':
    main()
