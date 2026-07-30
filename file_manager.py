import datetime
import os
from logger import log_command, log_error
from voice import speak
from PIL import ImageGrab

SCREENSHOT_DIR = os.path.join(os.getcwd(), "Screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def open_special_folder(folder_name):
    user_home = os.path.expanduser("~")
    folder_map = {
        "downloads": os.path.join(user_home, "Downloads"),
        "documents": os.path.join(user_home, "Documents"),
        "desktop": os.path.join(user_home, "Desktop"),
        "pictures": os.path.join(user_home, "Pictures"),
        "photos": os.path.join(user_home, "Pictures"),
    }

    target_dir = folder_map.get(folder_name.lower().strip())
    if target_dir and os.path.exists(target_dir):
        speak(f"Opening {folder_name.capitalize()} folder.")
        os.startfile(target_dir)
        log_command(f"open {folder_name}", f"Opened folder {target_dir}")
    else:
        speak(f"Folder {folder_name} not found.")

def search_file(query):
    filename = query.replace("search file", "").replace("find file", "").replace("search", "").strip()
    if not filename:
        speak("What is the name of the file you want to search for?")
        return

    speak(f"Searching for {filename}...")
    user_home = os.path.expanduser("~")
    matches = []

    search_roots = [
        os.path.join(user_home, "Desktop"),
        os.path.join(user_home, "Downloads"),
        os.path.join(user_home, "Documents"),
        os.getcwd()
    ]

    for root_dir in search_roots:
        if os.path.exists(root_dir):
            for root, dirs, files in os.walk(root_dir):
                for f in files:
                    if filename.lower() in f.lower():
                        matches.append(os.path.join(root, f))
                        if len(matches) >= 5:
                            break
                if len(matches) >= 5:
                    break

    if matches:
        speak(f"Found {len(matches)} matching file(s).")
        print("\n--- Matching Files ---")
        for match in matches:
            print("Found:", match)
        log_command(query, f"Found {len(matches)} files matching {filename}")
    else:
        speak(f"No file matching '{filename}' was found in your standard directories.")

def create_folder(query):
    folder_name = query.replace("create folder", "").replace("new folder", "").replace("make folder", "").strip()
    if not folder_name:
        speak("What should the new folder be named?")
        return

    target_path = os.path.join(os.getcwd(), folder_name)
    try:
        os.makedirs(target_path, exist_ok=True)
        msg = f"Folder '{folder_name}' created successfully."
        speak(msg)
        print(f"Created directory: {target_path}")
        log_command(query, msg)
    except Exception as e:
        log_error(f"Create folder error for {folder_name}", e)
        speak(f"Failed to create folder {folder_name}.")

def delete_file(query):
    filename = query.replace("delete file", "").replace("remove file", "").strip()
    if not filename:
        speak("Which file would you like to delete?")
        return

    filepath = filename if os.path.isabs(filename) else os.path.join(os.getcwd(), filename)

    if not os.path.exists(filepath):
        speak(f"File '{filename}' does not exist.")
        return

    speak(f"Are you sure you want to permanently delete {os.path.basename(filepath)}? Say yes to confirm.")
    print(f"\nCONFIRMATION REQUIRED: Permanently delete '{filepath}'? (yes/no)")
    confirm = input("Confirm deletion (yes/no): ").strip().lower()

    if confirm in ["yes", "y"]:
        try:
            os.remove(filepath)
            msg = f"File {os.path.basename(filepath)} deleted successfully."
            speak(msg)
            log_command(query, msg)
        except Exception as e:
            log_error(f"File deletion error for {filepath}", e)
            speak("Failed to delete file.")
    else:
        speak("File deletion cancelled.")
        log_command(query, "File deletion cancelled by user.")

def rename_file(query):
    parts = query.replace("rename file", "").replace("rename", "").strip().split(" to ")
    if len(parts) < 2:
        speak("Please specify rename command as: rename file [old name] to [new name]")
        return

    old_name = parts[0].strip()
    new_name = parts[1].strip()

    old_path = old_name if os.path.isabs(old_name) else os.path.join(os.getcwd(), old_name)
    new_path = new_name if os.path.isabs(new_name) else os.path.join(os.getcwd(), new_name)

    if not os.path.exists(old_path):
        speak(f"File '{old_name}' not found.")
        return

    try:
        os.rename(old_path, new_path)
        msg = f"Renamed '{old_name}' to '{new_name}' successfully."
        speak(msg)
        log_command(query, msg)
    except Exception as e:
        log_error(f"Rename error: {old_name} -> {new_name}", e)
        speak("Failed to rename file.")

def take_screenshot():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(SCREENSHOT_DIR, f"screenshot_{timestamp}.png")

    try:
        try:
            import pyautogui
            screenshot = pyautogui.screenshot()
        except Exception:
            screenshot = ImageGrab.grab()

        screenshot.save(filepath)
        msg = f"Screenshot saved as screenshot_{timestamp}.png in Screenshots directory."
        speak("Screenshot captured successfully.")
        print(f"Saved: {filepath}")
        log_command("take screenshot", msg)
    except Exception as e:
        log_error("Screenshot error", e)
        speak("Failed to capture screenshot.")
