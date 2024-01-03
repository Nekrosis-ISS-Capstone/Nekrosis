"""
__init__.py: Entry point for the CouchCrasher library.

Library usage:
    >>> from couchcrasher import CouchCrasher
    >>> couchcrasher = CouchCrasher(payload="/path/to/payload")

    >>> couchcrasher.supported_persistence_methods()
    >>> couchcrasher.recommended_persistence_method()
    >>> couchcrasher.install()
"""

__version__:  str = "0.0.1"
__license__:  str = "3-clause BSD License"
__author__:   str = "Ezra Fast, Mitchell Nicholson, Mykola Grymalyuk, Scott Banister and Ulysses Hill"
__all__:     list = ["CouchCrasher"]

from .core import CouchCrasher, main