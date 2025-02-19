import os
import shutil

DOWNLOADS_FOLDER = "downloads"

def clear_download_folder():
    """Deletes all files in the downloads folder to prevent duplicate images."""
    if os.path.exists(DOWNLOADS_FOLDER):
        shutil.rmtree(DOWNLOADS_FOLDER)  # Delete the folder and its contents
        print(f"🗑️ Cleared '{DOWNLOADS_FOLDER}' folder.")

    # Recreate the folder
    os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)
    print(f"📂 New '{DOWNLOADS_FOLDER}' folder created.")

if __name__ == "__main__":
    clear_download_folder()

