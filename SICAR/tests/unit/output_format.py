import unittest
from SICAR import OutputFormat


class OutputFormatTestCase(unittest.TestCase):
    def test_shapefile_format(self):
        self.assertEqual(OutputFormat.SHAPEFILE, "shapefile")

    def test_csv_format(self):
        self.assertEqual(OutputFormat.CSV, "csv")

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            # Attempting to create an instance with an invalid format
            OutputFormat("invalid")
