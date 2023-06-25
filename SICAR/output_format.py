from enum import Enum


class OutputFormat(str, Enum):
    """
    Enumeration for output formats.

    Options:
        - SHAPEFILE: Shapefile format.
        - CSV: Comma-separated values format.
    """

    SHAPEFILE = "shapefile"
    CSV = "csv"
