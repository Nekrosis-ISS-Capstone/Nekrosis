# Couch-Crasher-Code

Repository for the Couch Crasher application. Information Systems Security Capstone Project for Winter 2024.

## Project Goals

* Multi-platform persistence toolkit.
   * Windows
   * Linux
   * macOS
* Written in Python 3.
* Supports providing payload for persistence.
* Determines best persistence method based on OS and current user privileges.
* Develop malware sample to test persistence toolkit.


## Project Architecture

- `couchcrasher.py`: Entry point for the Couch Crasher application.
  - Handle command line arguments.
  - Detect correct library to use (OS-specific).
  - Detect user privileges, pass to library.
  - Validate payload.
  - Call library to perform persistence.
- `core.py`: Parent class for OS-specific persistence classes.
  - Defines structures such as required methods for child classes.
  - Public functions (child classes must implement):
    - `supported_persistence_methods()`: Returns a list of supported persistence methods.
    - `configured_persistence_method()`: Returns the persistence method currently in use.
    - `install()`: Installs payload for persistence.
- `windows.py`: Windows-specific persistence class.
  - Inherits from `core.py`.
  - User privileges are determined by SID (Security Identifier).
- `linux.py`: Linux-specific persistence class.
  - Inherits from `core.py`.
  - User privileges are determined by EUID (Effective User Identifier).
- `macos.py`: macOS-specific persistence class.
  - Inherits from `core.py`.
  - User privileges are determined by EUID (Effective User Identifier).
