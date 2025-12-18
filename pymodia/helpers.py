import numpy as np
import os, json
from .fragment import MoDiaFragment
from .molecule import MoDiaMolecule

def autobuild_from_pyqint(res, name=None):
    """
    Try to auto-build Molecule and Fragments from results object
    """
    # grab atoms
    atoms, idx = np.unique([n[1] for n in res['nuclei']], return_index=True)
    atoms = atoms[np.argsort(idx)]
    
    # sneaky hack to handle homonuclear diatomic molecules
    if len(atoms) == 1 and len(res['nuclei']) == 2:
        atoms = [atoms[0],-1]
        res['nuclei'][1][1] = -1

    if len(atoms) != 2:
        raise Exception('Cannot autobuild from molecule with more than 2 distinct elements.')

    with open(os.path.join(os.path.dirname(__file__), 'atom_data.json'), "r") as f:
        data = json.load(f)

    def find_by_atomic_number(number):
        """
        Auxiliary method to find element by its number
        """
        return next(
            (v for v in data.values() if v.get("atomic_number") == number),
            None
        )

    # auto-build mapping
    mapping = {i:{} for i in atoms}
    ao_ids = {i:[] for i in atoms}
    for k,cgf in enumerate(res['cgfs']):
        for n in res['nuclei']:
            if np.allclose(cgf.p, n[0]):

                # build CGF identifier
                c_ident = []
                for g in cgf.gtos:
                    c_ident.append(g.c)
                    c_ident.append(g.alpha)
                    c_ident.append(g.l)
                    c_ident.append(g.m)
                    c_ident.append(g.n)

                # verify if identifier is known
                found = False
                for j,c in enumerate(ao_ids[n[1]]):
                    if np.allclose(c, c_ident):
                        found = True
                        mapping[n[1]][k] = j
                        break
                
                # add it if not found
                if not found:
                    mapping[n[1]][k] = len(ao_ids[n[1]])
                    ao_ids[n[1]].append(c_ident)

                break
    
    # in the case of homonuclear system, unspoof the second atom
    if atoms[1] == -1:
        res['nuclei'][1][1] = res['nuclei'][0][1]

    # fragment 1
    el = find_by_atomic_number(atoms[0])
    f1 = MoDiaFragment(el['symbol'], el['ao_energy'], el['atomic_number'], mapping[atoms[0]], sublabel=superscript(el['configuration']))
                       
    # fragment 2
    el = find_by_atomic_number(atoms[1] if atoms[1] != -1 else atoms[0]) # needed for homonuclear diatomic molecules
    f2 = MoDiaFragment(el['symbol'], el['ao_energy'], el['atomic_number'], mapping[atoms[1]], sublabel=superscript(el['configuration']))

    # molecule
    mol = MoDiaMolecule(name, res['orbe'], res['orbc'], res['nelec'])

    return mol, f1, f2

def subscript(string_in):
    """
    Function to turn all numbers in string to subscript
    """
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    string_out = string_in.translate(SUB)

    return string_out

def superscript(string_in):
    """
    Function to turn all numbers with ^in front in string to superscript
    """
    sup = False
    string_out = ""
    for element in string_in:
        if sup == True:
            SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
            sup_element = element.translate(SUP)
            sup = False
            string_out += sup_element
        elif element == "^":
            sup = True
        else:
            string_out += element

    return string_out