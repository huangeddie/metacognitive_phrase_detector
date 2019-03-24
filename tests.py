import unittest
import os

from algorithm import algorithm
from algorithm.data import Connotation


class TestMetaCognition(unittest.TestCase):

    def single_connotation_test(self, expected_connotation, file_path):
        with open(file_path) as f:
            for line in f:
                text = line.strip()
                phrases, _ = algorithm.analyze_text(text)

                if expected_connotation is None:
                    self.assertEqual(len(phrases), 0, text)
                else:
                    self.assertEqual(len(phrases), 1, '{} | {}'.format(text, phrases))
                    phrase = phrases[0]
                    self.assertEqual(phrase.connotation, expected_connotation, phrase)

    def test_single_negative_phrases(self):
        self.single_connotation_test(Connotation.NEGATIVE, 'algorithm/tests/single_negative_phrases')

    def test_single_positive_phrases(self):
        self.single_connotation_test(Connotation.POSITIVE, 'algorithm/tests/single_positive_phrases')

    def test_nothing(self):
        self.single_connotation_test(None, 'algorithm/tests/no_phrases')
        
        
if __name__ == '__main__':

    unittest.main()