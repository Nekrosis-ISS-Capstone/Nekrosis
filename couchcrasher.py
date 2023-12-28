"""
couchcrasher.py: Entry point for the CouchCrasher application.

Standalone usage:
    >>> couchcrasher.py (-p | --payload) <payload> [--method <method>]
    >>> couchcrasher.py (-h | --help)
    >>> couchcrasher.py (-v | --version)

Library usage:
    >>> from couchcrasher import CouchCrasher
    >>> couchcrasher = CouchCrasher(payload="/path/to/payload")

    >>> couchcrasher.supported_persistence_methods()
    >>> couchcrasher.recommended_persistence_method()
    >>> couchcrasher.run()
"""

import os
import sys
import argparse
import subprocess

from pathlib import Path

from support.core    import Persistence
from support.windows import WindowsPersistence
from support.linux   import LinuxPersistence
from support.macos   import MacPersistence


PROJECT_VERSION: str  = "0.0.1"

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


class CouchCrasher:
    """
    Main class for the CouchCrasher application.
    """

    def __init__(self, payload: str, custom_method: str = None) -> None:
        self._payload       = payload
        self._custom_method = custom_method

        self._identifier = self._get_privileges()
        self._current_os = self._get_os()

        if self._current_os not in SUPPORTED_HOSTS:
            raise NotImplementedError(f"OS {self._current_os} is not supported.")

        self._friendly_os_name = FRIENDLY_HOSTS[self._current_os]

        self.persistence_obj: Persistence = SUPPORTED_HOSTS[self._current_os](
            payload=self._payload,
            identifier=self._identifier,
            custom_method=self._custom_method
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
        - Windows: returns the Secure Identifier (SID) of the current user.
        """
        if hasattr(os, "geteuid"):
            return os.geteuid()

        user = os.getlogin()
        results = subprocess.run(
            ["powershell", "-Command", f"Get-WMIObject win32_useraccount -Filter \"Name='{user}'\" | Select SID"],
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


    def run(self) -> None:
        """
        Install the payload.
        """
        self._verify_payload()

        print("Creating persistence")
        print(f"  Payload: {self._payload}")
        print(f"  OS: {self._friendly_os_name}")
        print((f"  Effective User ID:" if self._current_os != "win32" else "  Security Identifier:") + f" {self._identifier}")
        print(f'  Persistence Method: "{self.persistence_obj.configured_persistence_method()}"')

        self.persistence_obj.install()


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


    def _list_supported_persistence_methods(self) -> None:
        """
        Get a list of supported persistence methods for the current OS.
        """
        print(f"Supported persistence methods for {self._friendly_os_name}:")
        for method in self.supported_persistence_methods():
            print(f'  "{method}"')

        print(f"\nRecommended persistence method for {self._friendly_os_name}:")
        print(f'  "{self.recommended_persistence_method()}"')

        print(f"\nIf missing methods, re-run with elevated privileges (if applicable).")


if __name__ == "__main__":
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
        version=f"CouchCrasher v{PROJECT_VERSION}",
    )
    parser.add_argument(
        "-l",
        "--list-supported-methods",
        action="store_true",
        help="List the supported persistence methods for the current OS."
    )


    args = parser.parse_args()

    couchcrasher = CouchCrasher(
        payload=args.payload,
        custom_method=args.method
    )

    if args.list_supported_methods:
        couchcrasher._list_supported_persistence_methods()
    else:
        if not args.payload:
            parser.print_help()
            exit(1)
        couchcrasher.run()