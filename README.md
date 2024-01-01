# Couch-Crasher-Code

A multi-platform persistence toolkit, with the goal of simplifying malware deployment.

Developed as a capstone project for the Southern Alberta Institute of Technology's Information Systems Security program (Winter 2024), to demonstrate the many techniques that can be used to achieve persistence on Windows, macOS, and Linux.

Please use irresponsibly.


## Setup

Requires Python 3.6 or newer, install from official website when applicable: [python.org](https://www.python.org/downloads/).

Additional dependencies can be installed with pip:
```sh
python -m pip install -r requirements.txt
```


## Usage

Project designed to be used either as a library or as a standalone executable.

### Library

```python
from couchcrasher import CouchCrasher

couchcrasher = CouchCrasher("/path/to/malware")

couchcrasher.supported_persistence_methods()
couchcrasher.recommended_persistence_method()
couchcrasher.run()
```


### Executable - Help
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

### Executable - Install Payload

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

## Authors

* [Ezra Fast](https://github.com/EzraFast1)
* [Mitchell Nicholson](https://github.com/1Kalagen1)
* [Mykola Grymalyuk](https://github.com/khronokernel)
* [Scott Banister](https://github.com/pleasantriess)
* [Ulysses Hill](https://github.com/Ulysses-Hill)