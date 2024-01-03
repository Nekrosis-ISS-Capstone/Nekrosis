"""
os_versioning.py: macOS versioning breakdown.
"""

import enum


class XNUVersions(enum.Enum):
    """
    XNU versions.
    """
    SONOMA:        int = 23
    VENTURA:       int = 22
    MONTEREY:      int = 21
    BIG_SUR:       int = 20
    CATALINA:      int = 19
    MOJAVE:        int = 18
    HIGH_SIERRA:   int = 17
    SIERRA:        int = 16
    EL_CAPITAN:    int = 15
    YOSEMITE:      int = 14
    MAVERICKS:     int = 13
    MOUNTAIN_LION: int = 12
    LION:          int = 11
    SNOW_LEOPARD:  int = 10
    LEOPARD:       int = 9
    TIGER:         int = 8
    PANTHER:       int = 7
    JAGUAR:        int = 6
    PUMA:          int = 5
    CHEETAH:       int = 4 # Technically 1.3.1