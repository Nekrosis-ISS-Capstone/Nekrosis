"""
linux.py: Linux-specific persistence logic.
"""

from .base                                import Persistence

from .linux_utilities.persistence_methods import LinuxPersistenceMethods

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


    def _determine_recommended_persistence_method(self) -> str:

        if self.identifier == UnixPrivilege.ROOT.value:
            return LinuxPersistenceMethods.CRONJOB_ROOT.value

        return LinuxPersistenceMethods.CRONJOB_USER.value


    def supported_persistence_methods(self) -> list:

        methods = [method.value for method in LinuxPersistenceMethods]
        if self.identifier != UnixPrivilege.ROOT.value:
            methods.remove(LinuxPersistenceMethods.CRONJOB_ROOT.value)

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

        raise NotImplementedError(f"Method {method} not implemented.")