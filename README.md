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


## Setup

Requires Python 3.6+, please install from official website: [python.org](https://www.python.org/downloads/).


```sh
# Base dependencies
pip install -r requirements.txt

# If creating standalone executable, install pyinstaller
pip install pyinstaller
```


## Usage

#### Help
```
$ couchcrasher.py (-h | --help)

>>> usage: couchcrasher [-h] [-p PAYLOAD] [-m METHOD] [-v] [-l]
>>>
>>> Install a payload for persistence on Windows, macOS, or Linux.
>>>
>>> options:
>>>   -h, --help            show this help message and exit
>>>   -p PAYLOAD, --payload PAYLOAD
>>>                         The payload to install.
>>>   -m METHOD, --method METHOD
>>>                         The custom persistence method to use (optional).
>>>   -v, --version         show program's version number and exit
>>>   -l, --list-supported-methods
>>>                         List the supported persistence methods for the current OS.
```


#### Version

```
$ couchcrasher.py (-v | --version)

>>> CouchCrasher v0.0.1
```


#### List Supported Methods

Dependant on OS and privileges of current user.
```
$ couchcrasher.py (-l | --list-supported-methods)

>>> Supported persistence methods for macOS:
>>>   "LaunchAgent - Current User"
>>>   "LaunchAgent - Library"
>>>   "LaunchDaemon - Library"
>>>
>>> Recommended persistence method for macOS:
>>>   "LaunchDaemon - Library"
>>>
>>> If missing methods, re-run with elevated privileges (if applicable).
```


#### Install Payload

Best method determined by privilege and other environmental factors if no method is specified.
```
$ couchcrasher.py (-p | --payload) <malware> (-m | --method) <method>

>>> Creating persistence
>>>   Payload: <malware>
>>>   OS: macOS
>>>   Effective User ID: 501
>>>   Persistence Method: "LaunchAgent - Current User"
>>> Installing launch service (LaunchAgent - Current User)
>>>   Relocated payload: /Users/target/Library/LaunchAgents/713753
>>>   Service file: /Users/target/Library/LaunchAgents/com.80309.plist
>>>   Service started successfully 🎉
```