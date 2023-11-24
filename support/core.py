"""
core.py: Class Structure for OS persistence logic.
"""

class Persistence:

    def __init__(self, payload: str, effective_user_id: int) -> None:
        self.payload = payload
        self.effective_user_id = effective_user_id


    def recommended_persistence_method(self) -> str:
        """
        Get the best persistence method for the current OS.
        """
        raise NotImplementedError(f"No implemented in current class: {self.__class__.__name__}")


    def install(self) -> None:
        """
        Install the payload.
        """
        raise NotImplementedError(f"No implemented in current class: {self.__class__.__name__}")