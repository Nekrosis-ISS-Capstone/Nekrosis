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

## 0.0.1
- Initial release.