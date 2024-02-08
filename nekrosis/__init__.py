"""
__init__.py: Entry point for the Nekrosis library.

Library usage:
    >>> from nekrosis import Nekrosis
    >>> nekrosis = Nekrosis(payload="/path/to/payload")

    >>> nekrosis.supported_persistence_methods()
    >>> nekrosis.recommended_persistence_method()
    >>> nekrosis.install()
"""

__title__:        str = "nekrosis"
__version__:      str = "0.0.2"
__description__:  str = "Multi-platform persistence toolkit for user-provided payloads."
__url__:          str = "https://github.com/Nekrosis-ISS-Capstone/Nekrosis"
__license__:      str = "3-clause BSD License"
__author__:       str = "Ezra Fast, Mitchell Nicholson, Mykola Grymalyuk, Scott Banister and Ulysses Hill"
__author_email__: str = "nekrosis-capstone@protonmail.com"
__status__:       str = "Alpha"
__all__:         list = ["Nekrosis"]

from .core import Nekrosis, main