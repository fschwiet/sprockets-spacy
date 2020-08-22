import unittest

from tests.context import *


class TestConjugationFeatures(unittest.TestCase):
    def test_can_detect_subjunctivity(self):
        self.assertEqual(False, sprocketry.spanish_conjugations.get().has_subjunctivity("vas", "ir"))
        self.assertEqual(True, sprocketry.spanish_conjugations.get().has_subjunctivity("vayas", "ir"))


if __name__ == '__main__':
    unittest.main()