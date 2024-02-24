"""
core.py: Class Structure for OS persistence logic.
"""

import logging
import tempfile


class Persistence:
    """
    Base class for OS-specific persistence logic.

    Parameters:
        payload:            The payload to install.
        identifier:         The effective user ID on Unix, or administrator status (UAC) on Windows.
        custom_method:      The custom persistence method to use.
    """

    def __init__(self, payload: str, identifier: int, custom_method: str = None) -> None:
        self.payload = payload
        self.identifier = identifier
        self.custom_method = custom_method

        self.recommended_method = None

        self.temp_dir = tempfile.TemporaryDirectory()


    def __post_init__(self) -> None:
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

            try:
                self.custom_method = self._convert_index_to_method(methods, int(self.custom_method))
            except ValueError:
                pass

            if self.custom_method not in methods:
                raise ValueError(f"Custom method {self.custom_method} is not supported.\nSupported methods:\n" + "\n".join([f'  {i} - "{method}"' for i, method in enumerate(methods)]))
            return self.custom_method

        return self.recommended_method


    def _convert_index_to_method(self, methods: list, index: int) -> str:
        """
        Convert an index to a method.
        """
        if index < 0 or index > len(methods) - 1:
            raise ValueError(f"Index {index} is out of range (0-{len(methods) - 1}).")
        return methods[index]


    def install(self) -> None:
        """
        Install the payload.
        """
        logging.critical(f"install() not implemented in current class ({self.__class__.__name__})")