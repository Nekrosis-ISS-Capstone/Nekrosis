# Nekrosis Design

Project is designed such that it can be used as follows:
- Library: Importable into larger projects (ex. Nekrosis-GUI).
- Executable: Standalone executable for use in scripts or on the command line.

As such, avoid interactions with users post-invocation (ex. `input()`). If additional information must be gathered, use command line arguments or a configuration file.

Additionally, the project must be usable with simply a single payload and no other input. There must be default values for all required parameters, and logic for best method determination must be implemented.

Finally all print statements must uses the `logging` module to allow for silent operation.


## Structure

- [`nekrosis/core.py`](../nekrosis/core.py): Entry point for the Nekrosis application.
  - Handle command line arguments.
  - Detect correct library to use (OS-specific).
  - Detect user privileges, pass to library.
  - Validate payload.
  - Call library to perform persistence.
- [`nekrosis/support/base.py`](../nekrosis/support/base.py): Parent class for OS-specific persistence classes.
  - Defines structures such as required methods for child classes.
  - Public functions (child classes must implement):
    - `supported_persistence_methods()`: Returns a list of supported persistence methods.
    - `configured_persistence_method()`: Returns the persistence method currently in use.
    - `install()`: Installs payload for persistence.
- [`nekrosis/support/windows.py`](../nekrosis/support/windows.py): Windows-specific persistence class.
  - Inherits from `base.py`.
  - User privileges are determined by administrator status (UAC).
- [`nekrosis/support/linux.py`](../nekrosis/support/linux.py): Linux-specific persistence class.
  - Inherits from `base.py`.
  - User privileges are determined by EUID (Effective User Identifier).
- [`nekrosis/support/macos.py`](../nekrosis/support/macos.py): macOS-specific persistence class.
  - Inherits from `base.py`.
  - User privileges are determined by EUID (Effective User Identifier).