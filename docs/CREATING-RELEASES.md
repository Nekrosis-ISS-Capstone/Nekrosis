# Creating new GitHub and PyPI releases

This document outlines the process for creating new releases for Nekrosis. Note that PyPI releases are automatically created by GitHub Actions when a new release is created on GitHub.

1. Select `Releases` from the GitHub repository.
2. Click `Draft a new release`.
3. Enter the tag version (e.g. `1.1.0`) and a title (e.g. `1.1.0`).
4. Copy CHANGELOG.md for the release notes.
5. Click `Publish release`.

Once complete, edit [`nekrosis/__init__.py`](../nekrosis/__init__.py) to reflect the new version number (e.g. `__version__ = "1.2.0"`).