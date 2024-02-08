"""
interpreter.py: Resolve application-specific properties.
"""

import sys

from functools import cached_property


class ExecutableProperties:

    def __init__(self):
        pass


    @cached_property
    def application_entry_point(self) -> str:
        """
        Get the application entry point.

        Always returns relative path.

        Sample output:
        - PyInstaller: ./nekrosis
        - Python:      ./nekrosis.py
        """
        return sys.argv[0]


    @cached_property
    def interpreter(self) -> str:
        """
        Get the Python interpreter.

        Always returns full path.

        Sample output:
        - PyInstaller: /Users/username/nekrosis
        - Python:      /Library/Frameworks/Python.framework/Versions/3.12/bin/python3
        """
        return sys.executable


    @cached_property
    def is_project_pip_installed(self) -> bool:
        """
        Check if the project is installed via pip.

        Returns True if installed via pip, False otherwise.
        """
        return "site-packages" in __file__
