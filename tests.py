import unittest
import main


class TestCrossing(unittest.TestCase):
    FIELD_PATH = r'C:\Users\stoyan\Desktop\Работа\points_for_scripts'
    OBJECT_PATH = r'C:\Users\stoyan\Desktop\Работа\oopt'
    ANSWER = "[['', 'Point', 'Total'], ['RU-AL', 13, 13]]"

    def test_crossing_borders(self):
        self.assertEqual(str(main.crossing_borders(self.FIELD_PATH, self.OBJECT_PATH)), self.ANSWER)


if __name__ == '__main__':
    unittest.main()
