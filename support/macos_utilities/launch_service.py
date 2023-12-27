"""
launch_service.py: macOS-specific launchd logic.
"""
import os
import random
import plistlib
import subprocess

from pathlib import Path

from support.macos_utilities.persistence_methods import MacPersistenceMethods


BIN_CP:        str = "/bin/cp"
BIN_CHMOD:     str = "/bin/chmod"
BIN_LAUNCHCTL: str = "/bin/launchctl"
BIN_ID:        str = "/usr/bin/id"
BIN_CHOWN:     str = "/usr/sbin/chown"


class LaunchService:

    def __init__(self, payload: str) -> None:
        self.payload = payload


    def _current_user_id(self) -> str:
        """
        Get the current user's ID.
        """
        return subprocess.run([BIN_ID, "-u", os.getlogin()], capture_output=True, text=True).stdout.strip()


    def _build_launch_service(self, name: str, arguments: list, enviroment_variables: dict = None) -> dict:
        """
        Build a launch service.

        Source:
        - https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html
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
            return self._start_launch_agent(service_path)
        elif Path(service_path).parent.name == "LaunchDaemons":
            return self._start_launch_daemon(service_path)

        raise ValueError(f"Unknown service path {service_path}")


    def _start_launch_agent(self, service_path: str) -> bool:
        """
        Start Launch Agent
        """
        current_user_id = self._current_user_id()

        commands = [
            [BIN_CHMOD, "644", service_path],
            [BIN_CHOWN, current_user_id, service_path],
            [BIN_LAUNCHCTL, "asuser", current_user_id, BIN_LAUNCHCTL, "load", "-w", service_path],
            [BIN_LAUNCHCTL, "asuser", current_user_id, BIN_LAUNCHCTL, "start", Path(service_path).stem]
        ]

        for command in commands:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
                return False

        return True


    def _start_launch_daemon(self, service_path: str) -> bool:
        """
        Start Launch Daemon
        """
        commands = [
            [BIN_CHMOD, "644", service_path],
            [BIN_CHOWN, "root:wheel", service_path],
            [BIN_LAUNCHCTL, "load", "-w", service_path],
            [BIN_LAUNCHCTL, "start", Path(service_path).stem]
        ]

        for command in commands:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
                return False

        return True


    def install_generic_launch_service(self, variant: str, randomize_name: bool = True) -> None:
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
        subprocess.run([BIN_CP, self.payload, str(payload_file)], capture_output=True, text=True)

        print(f"  Relocated payload: {payload_file}")
        print(f"  Service file: {service_file_path}")

        plistlib.dump(self._build_launch_service(name=service_name, arguments=[str(payload_file)]), service_file_path.open("wb"))

        if not self._start_launch_service(str(service_file_path)):
            raise RuntimeError("Failed to start launch service.")

        print("  Service started successfully 🎉")