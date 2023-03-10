import unittest
from pprint import pprint

from avral_crossing_borders import crossing_borders


class TestCrossing(unittest.TestCase):
    FIELD_PATH = r'tests\points_for_scripts'
    OBJECT_PATH = r'tests\oopt'
    ANSWER = "[['', 'Point', 'Total'], ['RU-AL', 13, 13]]"

    def test_crossing_borders(self):
        self.assertEqual(str(crossing_borders.crossing_borders(
            self.FIELD_PATH, self.OBJECT_PATH)), self.ANSWER)


if __name__ == '__main__':
    unittest.main()
