# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller Configuration File
"""

import platform

from PyInstaller.building.api import PYZ, EXE
from PyInstaller.building.build_main import Analysis


FILENAME:   str = "couchcrasher"
RUNNING_OS: str = platform.system()

if RUNNING_OS == "Windows":
    FILENAME += ".exe"


a = Analysis(['couchcrasher.py'],
    pathex=[],
    binaries=[],
    datas=[("support", '.')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=FILENAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    target_arch="universal2",
    console=True)