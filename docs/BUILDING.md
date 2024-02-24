# Building Nekrosis

While not required for development, the following commands can be used to build the project:
- Library: `python -m build --wheel`
  - Resulting wheel file can be found in `dist/`.
- Executable: `python -m pyinstaller nekrosis.spec`
  - Resulting executable can be found in `dist/`.

If there are any issues with building, please reference our CI/CD configuration: [.github/workflows/](../.github/workflows/).