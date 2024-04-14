# Nekrosis Changelog

## 0.1.0
- Linux changes/improvements:
  - Detect if `cron` is available before presenting it as an option.
  - Detect if distribution is `systemd`-based before presenting it as an option.
  - Avoid printing cronjob status to STDOUT.
- macOS changes/improvements:
  - Detect if `cron` is available before presenting it as an option.
  - Expanded Electron persistence method to support root persistence.
    - LaunchDaemon - Electron

## 0.0.3
- setup.py: Resolve local file references when publishing to PyPI
  - ex. images and file URLs
- Linux changes/improvements:
  - Add `Systemd`-based persistence method.
    - `SystemdService` (requires root)

## 0.0.2
- Windows changes/improvements:
  - Switch to admin detection via UAC for privilege status.
  - Add `Startup folder`-based persistence methods.
    - `Startup Folder (Current User)` (default)
    - `Startup Folder (All Users)` (requires admin)
  - Windows: Add `Registry`-based persistence method.
    - `RUNKEY` (requires admin)
  - Windows: Add `Shortcut`-based persistence method.
    - `Shortcut (Current User)`
- macOS/Linux changes/improvements:
  - Add `Cron`-based persistence method.
    - `Cron (Current User)`
    - `Cron (Root)` (requires root)
- General changes/improvements:
  - Add support for specifying persistence method as index in addition to name.
  - Add support for providing payload as a URL.
  - Rename Application Entry Point to `nekrosis.py` (from `nekrosis_entry.py`).
    - Does not affect library usage.
  - New arguments:
    - Add new `-n/--nuke` option to delete payload and Nekrosis on exit.
    - Add new `-s/--silent` option to suppress STDOUT/STDERR output.
    - Add new `-e/--export` option for exporting supported persistence methods to standardized formats.
      - Supported formats:
        - `JSON`
        - `XML`
        - `PLIST`
  - Publish new project metadata:
    - `__title__`
    - `__description__`
    - `__url__`
    - `__status__`
    - `__author_email__`

## 0.0.1
- Initial release.