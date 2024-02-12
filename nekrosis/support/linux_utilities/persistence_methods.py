"""
persistence_methods.py: Linux specific persistence methods
"""

import enum


class LinuxPersistenceMethods(enum.Enum):
    """
    Linux-specific persistence methods.
    """

    ROOTCRONJOB:    str = "Root Crontab Injection"

    SILLYSERVICE:   str = "Silly Service Injection"
