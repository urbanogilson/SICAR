"""
Output Format Enumeration Module.

This module defines an enumeration for output formats.

Enumerations:
    OutputFormat: Enumeration for output formats.
        - SHAPEFILE: Shapefile format.
        - CSV: Comma-separated values format.
"""

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
