# download_car/polygon.py
"""
Polygon Enumeration Module.

This module defines an enumeration representing DownloadCar polygons.

Enumerations:
    State: Enumeration representing DownloadCar polygons.
        - AREA_PROPERTY: Perímetros dos imóveis (Property perimeters)
        - APPS: Área de Preservação Permanente (Permanent preservation area)
        - NATIVE_VEGETATION: Remanescente de Vegetação Nativa (Native Vegetation Remnants)
        - CONSOLIDATED_AREA: Área Consolidada (Consolidated Area)
        - AREA_FALL: Área de Pousio (Fallow Area)
        - HYDROGRAPHY: Hidrografia (Hydrography)
        - RESTRICTED_USE: Uso Restrito (Restricted Use)
        - ADMINISTRATIVE_SERVICE: Servidão Administrativa (Administrative Servitude)
        - LEGAL_RESERVE: Reserva Legal (Legal reserve)
"""

from enum import Enum


class Polygon(str, Enum):
    """
    Enumeration representing DownloadCar polygons.

    Options:
        - AREA_PROPERTY: Perímetros dos imóveis (Property perimeters)
        - APPS: Área de Preservação Permanente (Permanent preservation area)
        - NATIVE_VEGETATION: Remanescente de Vegetação Nativa (Native Vegetation Remnants)
        - CONSOLIDATED_AREA: Área Consolidada (Consolidated Area)
        - AREA_FALL: Área de Pousio (Fallow Area)
        - HYDROGRAPHY: Hidrografia (Hydrography)
        - RESTRICTED_USE: Uso Restrito (Restricted Use)
        - ADMINISTRATIVE_SERVICE: Servidão Administrativa (Administrative Servitude)
        - LEGAL_RESERVE: Reserva Legal (Legal reserve)
    """

    AREA_PROPERTY = "AREA_IMOVEL"
    APPS = "APPS"
    NATIVE_VEGETATION = "VEGETACAO_NATIVA"
    CONSOLIDATED_AREA = "AREA_CONSOLIDADA"
    AREA_FALL = "AREA_POUSIO"
    HYDROGRAPHY = "HIDROGRAFIA"
    RESTRICTED_USE = "USO_RESTRITO"
    ADMINISTRATIVE_SERVICE = "SERVIDAO_ADMINISTRATIVA"
    LEGAL_RESERVE = "RESERVA_LEGAL"
