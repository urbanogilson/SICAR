# SICAR/tests/unit/url.py
import unittest
from SICAR import Polygon


class PolygonTestCase(unittest.TestCase):
    def test_enum_values(self):
        self.assertEqual(Polygon.AREA_PROPERTY, "AREA_IMOVEL")
        self.assertEqual(Polygon.APPS, "APPS")
        self.assertEqual(Polygon.NATIVE_VEGETATION, "VEGETACAO_NATIVA")
        self.assertEqual(Polygon.CONSOLIDATED_AREA, "AREA_CONSOLIDADA")
        self.assertEqual(Polygon.AREA_FALL, "AREA_POUSIO")
        self.assertEqual(Polygon.HYDROGRAPHY, "HIDROGRAFIA")
        self.assertEqual(Polygon.RESTRICTED_USE, "USO_RESTRITO")
        self.assertEqual(Polygon.ADMINISTRATIVE_SERVICE, "SERVIDAO_ADMINISTRATIVA")
        self.assertEqual(Polygon.LEGAL_RESERVE, "RESERVA_LEGAL")
