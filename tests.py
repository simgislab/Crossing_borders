import unittest
from pprint import pprint

import main


class TestCrossing(unittest.TestCase):
    FIELD_PATH = r'tests\points_for_scripts'
    OBJECT_PATH = r'tests\oopt'
    ANSWER = "[['', 'Point', 'Total'], ['RU-AL', 13, 13]]"

    def test_crossing_borders(self):
        self.assertEqual(str(main.crossing_borders(self.FIELD_PATH, self.OBJECT_PATH)), self.ANSWER)


if __name__ == '__main__':
    unittest.main()
