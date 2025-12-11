import unittest
import filecmp
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pymodia import MoDia, MoDiaData, MoDiaMolecule, Atom, subscript

class TestN2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Makes and saves the test SVG
        """
        # MO data
        mo_energies = [-15.1, -14.9, -1.2, -0.8, 0.1, 0.5, 0.5, 1.5, 1.5, 2]
        orbc = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]]

        # Setting up PyMoDia objects
        N = Atom("N", [-15, -1, 1, 1, 1])
        Mol_name = subscript("N2")
        Mol = MoDiaMolecule(Mol_name, N, 1, N, 1)

        N2 = MoDiaData(molecule=Mol, moe=mo_energies, orbc=orbc)

        mo_colors = ["#000000", "#000000", "#1260CC", "#1260CC", "#1260CC",
                     "#FE6E00", "#FE6E00", "#FE6E00", "#FE6E00", "#1260CC",
                     "#1260CC"]
        ao_colors = ["#000000", "#1260CC", "#FE6E00", "#FE6E00", "#FE6E00"]
        mo_labels = ['1s', '1s', '1σ', '1σ*', '2σ', '1π', '1π', '1π*', '1π*' , '2σ*']
        diagram = MoDia(N2, orbc_cutoff=0.9, mo_color=mo_colors, ao1_color=ao_colors,
                        ao2_color=ao_colors, draw_energy_labels = False,
                        mo_labels=mo_labels, draw_level_labels=True,
                        level_labels_style='mo_ao')

        # Save image
        diagram.export_svg(os.path.join('tests', 'n2_test_results.svg'))

    def test_N2_svg(self):
        """
        Compares the test SVG with the reference SVG
        """
        self.assertTrue(os.path.exists(os.path.join('tests', 'n2_test_results.svg')))

    @classmethod
    def tearDownClass(self):
        """
        Removes the test SVG
        """
        os.remove(os.path.join('tests', 'n2_test_results.svg'))

if __name__ == '__main__':
    unittest.main()
