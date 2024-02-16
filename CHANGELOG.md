# Nekrosis Changelog

## 0.0.2
- Windows: Switch to admin detection via UAC for privilege status.
- Windows: Add `Startup` folder-based persistence method.
  - `Startup Folder (Current User)` (default)
  - `Startup Folder (All Users)` (requires admin)
- Rename Application Entry Point to `nekrosis.py` (from `nekrosis_entry.py`).
  - Does not affect library usage.
- Add support for exporting supported persistence methods to standardized formats.
  - `JSON`
  - `XML`
  - `PLIST`
- Add support for specifying persistence method as index in addition to name.
- Add new `-n/--nuke` option to delete payload and Nekrosis on exit.
- Publish new project metadata:
  - `__title__`
  - `__description__`
  - `__url__`
  - `__status__`
  - `__author_email__`
- Add support for providing payload as a URL.
- Unix: Implement Cron-based persistence method.
  - Supports both Linux and macOS, for current user and root.
- Add new `-s/--silent` option to suppress STDOUT/STDERR output.

## 0.0.1
- Initial release.