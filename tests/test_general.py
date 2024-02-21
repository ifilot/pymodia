import unittest
import os
import sys

# add a reference to load the PPMIL library
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pymodia import Atom, subscript


class TestH2(unittest.TestCase):

    def test_Atom(self):

        H = Atom('H')
        self.assertEqual(H.atomic_number, 1)
        self.assertEqual(H.full_name, 'Hydrogen')
        self.assertEqual(H.configuration, '(1s¹)')
        self.assertEqual(H.energies, [-0.50])

        C = Atom('C')
        self.assertEqual(C.atomic_number, 6)
        self.assertEqual(C.full_name, 'Carbon')
        self.assertEqual(C.configuration, '(1s²2s²2p²)')
        self.assertEqual(C.energies, [-11.32, -0.71, -0.43, -0.43, -0.43])

    def test_subscript(self):
        self.assertEqual('H₂', subscript('H2'))
        self.assertNotEqual('H2', subscript('H2'))

        self.assertEqual('CH₄', subscript('CH4'))
        self.assertNotEqual('CH4', subscript('CH4'))

        self.assertEqual('C₆H₆', subscript('C6H6'))
        self.assertNotEqual('C6H6', subscript('C6H6'))


if __name__ == '__main__':
    unittest.main()
