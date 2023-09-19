import unittest
import filecmp
import os
import sys

# add a reference to load the PPMIL library
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pymodia import PyMoDia, Atom, Molecule, subscript

class TestH2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Makes and saves the test SVG
        """
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

        N = Atom("N", [-15, -1, 1, 1, 1])

        Mol_name = subscript("N2")

        N2 = Molecule(Mol_name, N, 1, N, 1)

        core_cutoff = -10
        contribution_cutoff = 0.9

        mo_colors = ["#000000", "#000000", "#1260CC", "#1260CC", "#1260CC",
                     "#FE6E00", "#FE6E00", "#FE6E00", "#FE6E00", "#1260CC",
                     "#1260CC"]
        ao_colors = ["#000000", "#1260CC", "#FE6E00", "#FE6E00", "#FE6E00"]

        diagram = PyMoDia(N2, mo_energies, orbc, core_cutoff)
        diagram.draw_levels(colors_mo=mo_colors,
                            colors_ao1=ao_colors, colors_ao2=ao_colors)
        diagram.draw_occupancies()
        diagram.draw_contributions(contribution_cutoff)
        diagram.image.save_svg(os.path.join('tests', 'n2_test_results.svg'))

    def test_H2_svg(self):
        """
        Compares the test SVG with the reference SVG
        """
        ref_svg = os.path.join('tests', 'reference', 'n2_test_ref.svg')
        test_svg = os.path.join('tests', 'n2_test_results.svg')

        self.assertTrue(filecmp.cmp(test_svg, ref_svg))

    @classmethod
    def tearDownClass(self):
        """
        Removes the test SVG
        """
        os.remove(os.path.join('tests', 'n2_test_results.svg'))

if __name__ == '__main__':
    unittest.main()
