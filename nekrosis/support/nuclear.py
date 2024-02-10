"""
nuclear.py: Clean all traces of Nekrosis and the original payload from host system.
"""

import os
import sys
import logging
import subprocess

from pathlib import Path

from .interpreter import ExecutableProperties

from .. import __title__, __status__


class Eradicate:
    """
    Clean all traces of Nekrosis and the original payload from host system.
    """

    def __init__(self, payload: str) -> None:
        self._payload = payload


    def all(self) -> None:
        """
        Remove all traces of Nekrosis and the original payload from the host system.
        """
        self.payload()
        self.core()


    def payload(self) -> None:
        """
        Remove the original payload.
        """
        logging.info(f"Removing payload: {self._payload}")
        self._nuke_payload()


    def _nuke_payload(self) -> None:
        """
        Internal method for removing the original payload.
        """
        os.remove(self._payload)


    def core(self) -> None:
        """
        Remove core library.
        """
        logging.info(f"Removing {__title__} core library.")
        if ExecutableProperties().is_project_pip_installed:
            self._nuke_core_library()
            return

        if ExecutableProperties().application_entry_point.endswith(".py"):
            self._nuke_core_source()
            return

        if hasattr(sys, "frozen"):
            self._nuke_core_frozen()
            return

        raise NotImplementedError("Unknown installation type.")


    def _nuke_core_frozen(self) -> None:
        """
        For frozen applications.
        """
        os.remove(ExecutableProperties().application_entry_point)


    def _nuke_core_library(self) -> None:
        """
        For library usage.
        """
        # Uninstall Nekrosis from pip
        subprocess.run(
            [
                ExecutableProperties().interpreter, "-m",
                "pip", "uninstall", "--yes", __title__,
            ]
        )

        # Check if nekrosis is still in the pip cache
        if __title__ not in subprocess.run(
            [
                ExecutableProperties().interpreter, "-m",
                "pip", "cache", "list",
            ],
            capture_output=True, text=True,
        ).stdout:
            return

        # Remove cached files
        subprocess.run(
            [
                ExecutableProperties().interpreter, "-m",
                "pip", "cache", "remove", __title__,
            ]
        )


    def _nuke_core_source(self) -> None:
        """
        For source usage.
        """
        if __status__ not in ["Production/Stable", "Mature", "Inactive"]:
            # Avoid nuking source directory if in development
            logging.warning(f"Skipping nuking of source directory due to {__status__} status.")
            return

        source_directory = Path(ExecutableProperties().application_entry_point).parent / __title__
        source_directory.rmdir()