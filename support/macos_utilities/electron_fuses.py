"""
Parse Electron Framework binary, resolve Fuses configuration

Based on @electron/fuses:
- https://github.com/electron/fuses

Usage:
    >>> from electron_fuses import FusesDetection
    >>> fuses = FusesDetection("Bitwarden")
    >>> fuses.vulnerable_to_run_as_node()
    True
"""


import enum
from pathlib import Path


# https://github.com/electron/fuses/blob/v1.7.0/src/constants.ts#L1
SENTINEL: str = "dL7pKGdnNz796PbbjQWNKmHXBZaB9tsX"


# https://github.com/electron/fuses/blob/v1.7.0/src/constants.ts#L3-L8
class FuseState(enum.Enum):
    DISABLE = 0x30
    ENABLE  = 0x31
    REMOVED = 0x72
    INHERIT = 0x90


# https://github.com/electron/fuses/blob/v1.7.0/src/config.ts#L8-L17
class FuseV1Options(enum.Enum):
    RUN_AS_NODE                               = 0
    ENABLE_COOKIE_ENCRYPTION                  = 1
    ENABLE_NODE_OPTIONS_ENVIRONMENT_VARIABLE  = 2
    ENABLE_NODE_CLI_INSPECT_ARGUMENTS         = 3
    ENABLE_EMBEDDED_ASAR_INTEGRITY_VALIDATION = 4
    ONLY_LOAD_APP_FROM_ASAR                   = 5
    LOAD_BROWSER_PROCESS_SPECIFIC_V8_SNAPSHOT = 6
    GRANT_FILE_PROTOCOL_EXTRA_PRIVILEGES      = 7


class FusesDetection:

    def __init__(self, file: str) -> None:
        self._electron_framework = self._resolve_electron_framework(file)


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
            fuse_config[i] = current_state

        return fuse_config


    def vulnerable_to_run_as_node(self) -> bool:
        """
        Check if the application is vulnerable to the run-as-node exploit

        Returns:
            bool: True if vulnerable, False otherwise
        """
        if self._electron_framework is None:
            return False

        fuse_config = self._fetch_fuse_state(self._electron_framework)

        return fuse_config[FuseV1Options.RUN_AS_NODE.value] == FuseState.ENABLE.value
