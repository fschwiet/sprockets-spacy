import unittest

from tests.context import *


class TestConjugationFeatures(unittest.TestCase):
    def test_can_detect_subjunctivity(self):
        self.assertEqual(False, sprocketry.spanish_conjugations.get().has_subjunctivity("vas", "ir"))
        self.assertEqual(True, sprocketry.spanish_conjugations.get().has_subjunctivity("vayas", "ir"))

    def test_can_get_conjugation_name(self):
        self.assertEqual("indicative/present", sprocketry.spanish_conjugations.get().get_conjugation_name("hablas", "hablar"))
        self.assertEqual("gerund", sprocketry.spanish_conjugations.get().get_conjugation_name("hablando", "hablar"))
        self.assertEqual("indicative/present|preterite", sprocketry.spanish_conjugations.get().get_conjugation_name("hablamos", "hablar"))
        self.assertEqual("indicative/present", sprocketry.spanish_conjugations.get().get_conjugation_name("prohíbo", "prohibir"))

if __name__ == '__main__':
    unittest.main()