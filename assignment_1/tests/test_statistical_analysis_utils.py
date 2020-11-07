import unittest
import numpy as np
from .. import statistical_analysis_utils

class MyTestCase(unittest.TestCase):
    def test_sample_mean(self):
        x = np.arange(1, 6, 1)
        self.assertEqual(statistical_analysis_utils.sample_mean(x), 3.)

    def test_sample_variance(self):
        x = np.arange(1, 6, 1)
        self.assertEqual(statistical_analysis_utils.sample_variance(x), 2.5)

        x = np.array([170, 300, 430, 470, 600])
        self.assertEqual(statistical_analysis_utils.sample_variance(x), 27130)

    def test_sample_standard_deviation(self):
        x = np.arange(1, 6, 1)
        self.assertEqual(statistical_analysis_utils.sample_standard_deviation(x), np.sqrt(10 / 4))

        x = np.array([170, 300, 430, 470, 600])
        self.assertEqual(statistical_analysis_utils.sample_standard_deviation(x), np.sqrt(27130))


if __name__ == '__main__':
    unittest.main()
