"""
core.py: Main class for the Nekrosis application.

Implemented as either a library through the Nekrosis class,
or as a standalone application through the main() function.
"""

import os
import sys
import logging
import argparse
import subprocess

from pathlib import Path

from nekrosis import __version__

from .support.base    import Persistence
from .support.windows import WindowsPersistence
from .support.linux   import LinuxPersistence
from .support.macos   import MacPersistence


SUPPORTED_HOSTS: dict = {
    "win32":  WindowsPersistence,
    "linux":  LinuxPersistence,
    "darwin": MacPersistence,
}

FRIENDLY_HOSTS:  dict = {
    "win32":  "Windows",
    "linux":  "Linux",
    "darwin": "macOS"
}


class Nekrosis:
    """
    Main class for the Nekrosis application.

    Public methods:
        - install()
        - change_payload()
        - change_custom_method()
        - supported_persistence_methods()
        - recommended_persistence_method()
    """

    def __init__(self, payload: str, custom_method: str = None) -> None:
        self._payload       = payload
        self._custom_method = custom_method

        self._init_logging()

        self.persistence_obj: Persistence = None

        self._identifier = self._get_privileges()
        self._current_os = self._get_os()

        if self._current_os not in SUPPORTED_HOSTS:
            raise NotImplementedError(f"OS {self._current_os} is not supported.")

        self._friendly_os_name = FRIENDLY_HOSTS[self._current_os]
        self._init_persistence()


    def _init_persistence(self) -> None:
        """
        Create the persistence object.
        """
        self.persistence_obj: Persistence = SUPPORTED_HOSTS[self._current_os](
            payload=self._payload,
            identifier=self._identifier,
            custom_method=self._custom_method
        )


    def _init_logging(self, verbose: bool = False) -> None:
        """
        Initialize logging.
        """
        if logging.getLogger().hasHandlers():
            return

        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s" if verbose is False else "[%(levelname)-8s] [%(filename)-20s]: %(message)s",
            handlers=[
                logging.StreamHandler()
            ]
        )


    def _verify_payload(self) -> None:
        """
        Verify that the payload exists.
        """
        if not Path(self._payload).exists():
            raise FileNotFoundError(f"Payload {self._payload} does not exist.")


    def _get_os(self) -> str:
        """
        Get the current OS.
        """
        return sys.platform


    def _get_privileges(self) -> int | str:
        """
        Get privileges for the current user.
        - Unix: returns the effective user ID.
        - Windows: returns the Security Identifier (SID) of the current user.
        """
        if hasattr(os, "geteuid"):
            return os.geteuid()

        user = os.getlogin()
        results = subprocess.run(
            ["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", "-Command", f"Get-WMIObject win32_useraccount -Filter \"Name='{user}'\" | Select SID"],
            capture_output=True,
            text=True
        ).stdout.strip().split("\n")

        if len(results) < 3:
            raise ValueError(f"Unexpected output from powershell:\n{results}")

        # Security Identifiers must start with "S-"
        # https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-identifiers
        if not results[2].startswith("S-"):
            raise ValueError(f"Unexpected output from powershell:\n{results}")

        return results[2]


    def _list_supported_persistence_methods(self) -> None:
        """
        Get a list of supported persistence methods for the current OS.
        """
        logging.info(f"Supported persistence methods for {self._friendly_os_name}:")
        for method in self.supported_persistence_methods():
            logging.info(f'  "{method}"')

        logging.info("")
        logging.info(f"Recommended persistence method for {self._friendly_os_name}:")
        logging.info(f'  "{self.recommended_persistence_method()}"')

        logging.info("")
        logging.info("If missing methods, re-run with elevated privileges (if applicable).")


    def install(self) -> None:
        """
        Install the payload.
        """
        self._verify_payload()

        logging.info("Creating persistence")
        logging.info(f"  Payload: {self._payload}")
        logging.info(f"  OS: {self._friendly_os_name}")
        logging.info((f"  Effective User ID:" if self._current_os != "win32" else "  Security Identifier:") + f" {self._identifier}")
        logging.info(f'  Persistence Method: "{self.persistence_obj.configured_persistence_method()}"')

        self.persistence_obj.install()


    def change_payload(self, payload: str) -> None:
        """
        Change the payload.
        """
        self._payload = payload
        self.persistence_obj.payload = payload


    def change_custom_method(self, custom_method: str) -> None:
        """
        Change the custom persistence method.
        """
        self._custom_method = custom_method
        self.persistence_obj.custom_method = custom_method


    def reload(self) -> None:
        """
        Save changes to the persistence object.
        """
        self._init_persistence()


    def supported_persistence_methods(self) -> list:
        """
        Get a list of supported persistence methods for the current OS.
        """
        return self.persistence_obj.supported_persistence_methods()


    def recommended_persistence_method(self) -> str:
        """
        Get the recommended persistence method for the current OS.
        """
        return self.persistence_obj.recommended_method


def main():
    """
    Entry point for standalone application.
    """

    parser = argparse.ArgumentParser(
        description="Install a payload for persistence on Windows, macOS, or Linux.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-p",
        "--payload",
        action="store",
        help="The payload to install."
    )
    parser.add_argument(
        "-m",
        "--method",
        help="The custom persistence method to use (optional)."
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Nekrosis v{__version__}",
    )
    parser.add_argument(
        "-l",
        "--list-supported-methods",
        action="store_true",
        help="List the supported persistence methods for the current OS."
    )


    args = parser.parse_args()

    nekrosis = Nekrosis(
        payload=args.payload,
        custom_method=args.method
    )

    if args.list_supported_methods:
        nekrosis._list_supported_persistence_methods()
    else:
        if not args.payload:
            parser.print_help()
            sys.exit(1)
        nekrosis.install()


if __name__ == "__main__":
    main()