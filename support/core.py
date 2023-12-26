"""
core.py: Class Structure for OS persistence logic.
"""

import tempfile


class Persistence:
    """
    Base class for OS-specific persistence logic.

    Parameters:
        payload:            The payload to install.
        identifier:         The effective user ID on Unix, or Security Identifier (SID) on Windows.
        custom_method:      The custom persistence method to use.
    """

    def __init__(self, payload: str, identifier: int | str, custom_method: str = None) -> None:
        self.payload = payload
        self.identifier = identifier
        self.custom_method = custom_method

        self.temp_dir = tempfile.TemporaryDirectory()

        self.recommended_method = self._determine_recommended_persistence_method()


    def _determine_recommended_persistence_method(self) -> str:
        """
        Determine the recommended persistence method for the current OS.
        """
        return f"_determine_recommended_persistence_method() not implemented in current class ({self.__class__.__name__})"


    def supported_persistence_methods(self) -> list:
        """
        Get a list of supported persistence methods for the current OS.
        """
        return [f"supported_persistence_methods() not implemented in current class ({self.__class__.__name__})"]


    def configured_persistence_method(self) -> str:
        """
        Get the best persistence method for the current OS.
        """
        if self.custom_method:
            methods = self.supported_persistence_methods()
            if self.custom_method not in methods:
                raise ValueError(f"Custom method {self.custom_method} is not supported.\nSupported methods:\n" + "\n".join([f'  "{method}"' for method in methods]))
            return self.custom_method

        return self.recommended_method


    def install(self) -> None:
        """
        Install the payload.
        """
        print(f"install() not implemented in current class ({self.__class__.__name__})")