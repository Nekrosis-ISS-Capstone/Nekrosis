"""
electron.py: macOS-specific Electron vulnerability detection.
"""

import os
import sys
import subprocess

from pathlib import Path

from .electron_fuses import FusesDetection


BIN_NM:      str = "/usr/bin/nm"
BIN_STRINGS: str = "/usr/bin/strings"

if hasattr(sys, "_MEIPASS"):
    BIN_NM      = os.path.join(sys._MEIPASS, "support/macos_binaries/nm")
    BIN_STRINGS = os.path.join(sys._MEIPASS, "support/macos_binaries/strings")
elif "site-packages" in __file__:
    BIN_NM      = os.path.join(os.path.dirname(os.path.dirname(__file__)), "macos_binaries/nm")
    BIN_STRINGS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "macos_binaries/strings")


class SearchElectron:

    def __init__(self, search_path: str = "/Applications") -> None:
        self._search_path = Path(search_path)


    def find_first_exploitable_application(self) -> Path:
        """
        Find the first exploitable Electron application.

        Returns a Path object to the first exploitable Electron application.
        """
        for application in self._search_path.glob("*.app/Contents/Frameworks/Electron Framework.framework/Versions/A/Electron Framework"):
            if self.application_is_vulnerable(application.parent.parent.parent.parent.parent.parent) is True:
                return application.parent.parent.parent.parent.parent.parent

        return None


    def search(self, return_first_hit: bool = False) -> list:
        """
        Search for Electron applications.

        Returns a list of paths to Electron applications.
        """
        applications: list = []
        for application in self._search_path.glob("*.app/Contents/Frameworks/Electron Framework.framework/Versions/A/Electron Framework"):
            applications.append(application.parent.parent.parent.parent.parent.parent)

            if return_first_hit:
                break

        return applications


    def _application_implements_run_as_node(self, application: Path) -> bool:
        """
        Check if an application implements the runAsNode method.

        Returns True if the application implements the runAsNode method, False otherwise.
        """
        for binary in application.glob("Contents/MacOS/*"):
            if not binary.is_file():
                continue
            if self._binary_has_electron_run_as_node(binary):
                return True
        return False


    def _application_has_fuses_mitigation(self, application: Path) -> bool:
        """
        Check if an application implements the fuses mitigation.

        Returns True if the application implements the fuses mitigation, False otherwise.
        """
        for binary in application.glob("Contents/MacOS/*"):
            if not binary.is_file():
                continue
            if self._binary_has_fuses_mitigation(binary):
                return True
        return False


    def application_is_vulnerable(self, application: Path) -> bool:
        """
        Check if an application is vulnerable to the run-as-node exploit.

        Returns True if the application is vulnerable, False otherwise.
        """
        # False positives
        if application in [Path("/Applications/Visual Studio Code.app")]:
            return False

        if self._application_implements_run_as_node(application) is False:
            return False

        if self._application_has_fuses_mitigation(application) is False:
            return True

        return FusesDetection(str(application)).vulnerable_to_run_as_node()


    def _binary_has_electron_run_as_node(self, binary: str) -> bool:
        """
        Check for "ELECTRON_RUN_AS_NODE" with strings
        """
        try:
            output = subprocess.check_output([BIN_STRINGS, binary], stderr=subprocess.DEVNULL)
            return b"ELECTRON_RUN_AS_NODE" in output
        except subprocess.CalledProcessError:
            return False


    def _binary_has_fuses_mitigation(self, binary: str) -> bool:
        """
        Check for "__ZN8electron5fuses18IsRunAsNodeEnabledEv" with nm
        """
        try:
            output = subprocess.check_output([BIN_NM, binary], stderr=subprocess.DEVNULL)
            return b"__ZN8electron5fuses18IsRunAsNodeEnabledEv" in output
        except subprocess.CalledProcessError:
            return False