"""
electron_fuses.py: Resolve Electron Fuses configuration

Based on @electron/fuses:
- https://github.com/electron/fuses

Usage:
    >>> from electron_fuses import FusesDetection
    >>> fuses = FusesDetection("Bitwarden.app")
    >>> fuses.vulnerable_to_run_as_node()
    True
"""

import enum

from pathlib import Path


# https://github.com/electron/fuses/blob/v1.7.0/src/constants.ts#L1
SENTINEL: str = "dL7pKGdnNz796PbbjQWNKmHXBZaB9tsX"


# https://github.com/electron/fuses/blob/v1.7.0/src/constants.ts#L3-L8
class FuseState(enum.Enum):
    DISABLE: int = 0x30
    ENABLE:  int = 0x31
    REMOVED: int = 0x72
    INHERIT: int = 0x90


# https://github.com/electron/fuses/blob/v1.7.0/src/config.ts#L8-L17
class FuseV1Options(enum.Enum):
    RUN_AS_NODE:                               int = 0
    ENABLE_COOKIE_ENCRYPTION:                  int = 1
    ENABLE_NODE_OPTIONS_ENVIRONMENT_VARIABLE:  int = 2
    ENABLE_NODE_CLI_INSPECT_ARGUMENTS:         int = 3
    ENABLE_EMBEDDED_ASAR_INTEGRITY_VALIDATION: int = 4
    ONLY_LOAD_APP_FROM_ASAR:                   int = 5
    LOAD_BROWSER_PROCESS_SPECIFIC_V8_SNAPSHOT: int = 6
    GRANT_FILE_PROTOCOL_EXTRA_PRIVILEGES:      int = 7


class FusesDetection:

    def __init__(self, file: str) -> None:
        self.fuse_config = None

        self._electron_framework = self._resolve_electron_framework(file)
        if self._electron_framework is None:
            return

        self.fuse_config = self._fetch_fuse_state(self._electron_framework)


    def _resolve_electron_framework(self, application: str) -> str:
        """
        Resolve the path to the Electron Framework
        """

        electron_path = Path(application) / "Contents" / "Frameworks" / "Electron Framework.framework" / "Electron Framework"
        if not electron_path.exists():
            return None

        return electron_path


    def _fetch_fuse_state(self, binary: str) -> dict:
        """
        Fetch configured fuses from electron binary
        """
        binary_contents = open(binary, "rb").read()

        fuse_wire_position = binary_contents.find(SENTINEL.encode("utf-8")) + len(SENTINEL)
        if fuse_wire_position - len(SENTINEL) == -1:
            raise Exception("Could not find sentinel")

        # Get the fuse wire version
        fuse_wire_length = binary_contents[fuse_wire_position + 1]

        # Get the fuse config
        fuse_config = {}
        for i in range(fuse_wire_length):
            idx = fuse_wire_position + 2 + i
            current_state = binary_contents[idx]
            fuse_config[FuseV1Options(i).name] = FuseState(current_state).name
        return fuse_config


    def vulnerable_to_run_as_node(self) -> bool:
        """
        Check if the application is vulnerable to the run-as-node exploit

        Returns:
            bool: True if vulnerable, False otherwise
        """
        if self._electron_framework is None:
            return False

        return self.fuse_config[FuseV1Options.RUN_AS_NODE.name] == FuseState.ENABLE.name
