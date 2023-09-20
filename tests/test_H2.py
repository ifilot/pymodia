import unittest
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
        mo_energies = [-0.58, 0.67]
        orbc = [[-0.55, -0.55], [1.21, -1.21]]

        H = Atom("H", [-0.08])

        Mol_name = subscript("H2")

        Mol = Molecule(Mol_name, H, 1, H, 1)

        core_cutoff = -10
        contribution_cutoff = 0.3

        outer_height = 200
        core_height = 20
        height = outer_height+core_height+100

        mo_colors = ["#1aa7ec", "#1aa7ec"]

        diagram = PyMoDia(Mol, mo_energies, orbc, outer_height=outer_height,
                          core_height=core_height, height=height,
                          core_cutoff=core_cutoff)
        diagram.draw_levels(colors_mo=mo_colors)
        diagram.draw_occupancies()
        diagram.draw_contributions(contribution_cutoff, print_coeff=True)
        diagram.image.save_svg(os.path.join('tests', 'h2_test_results.svg'))

    def test_H2_svg(self):
        """
        Compares the test SVG with the reference SVG
        """
        self.assertTrue(os.path.exists(os.path.join('tests', 'h2_test_results.svg')))

    @classmethod
    def tearDownClass(self):
        """
        Removes the test SVG
        """
        os.remove(os.path.join('tests', 'h2_test_results.svg'))


if __name__ == '__main__':
    unittest.main()
