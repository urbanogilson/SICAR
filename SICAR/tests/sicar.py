import unittest
from SICAR import Sicar


class TestSicarBase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._car = Sicar()

    def test_get(self):
        self.assertTrue(self._car._get(self._car.get_base_url()).ok)


if __name__ == "__main__":
    unittest.main()
