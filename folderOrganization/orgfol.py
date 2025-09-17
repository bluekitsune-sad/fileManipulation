import os
from datetime import datetime
import shutil

# Define the path to the downloads folder
downloads_folder = os.path.expanduser('~') + '/Downloads'

# Define file type categories
folders = {
    'images': ['.jpg', '.jpeg', '.png', '.gif'],
    'documents': ['.pdf', '.docx', '.txt', '.xls', '.ppt'],
    'videos': ['.mp4', '.mkv', '.avi', '.mov'],
    'archives': ['.zip', '.tar', '.rar', '.7z'],
    'others': []
}

# Create necessary folders if they don't exist
def create_folders():
    for folder in folders.keys():
        folder_path = os.path.join(downloads_folder, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

# Smart rename to avoid file name duplication by adding a timestamp
def smart_rename(file_name, folder):
    name, extension = os.path.splitext(file_name)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return f"{name}_{timestamp}{extension}"

# Move and rename files into corresponding folders
def move_files():
    for file in os.listdir(downloads_folder):
        file_path = os.path.join(downloads_folder, file)

        # Skip directories and temporary files
        if os.path.isdir(file_path) or file.endswith(('.tmp', '.crdownload')):
            continue

        moved = False
        
        # Check file extension and move to the corresponding folder
        for folder, extensions in folders.items():
            if any(file.endswith(ext) for ext in extensions):
                new_name = smart_rename(file, folder)
                destination = os.path.join(downloads_folder, folder, new_name)

                try:
                    shutil.move(file_path, destination)
                    print(f"Moved {file} -> {destination}")
                    moved = True
                    break
                
                except FileNotFoundError:
                    print(f"Skipped {file} because it was not found or already deleted.")
                    continue
        
        # If no match was found, move the file to 'others'
        if not moved:
            new_name = smart_rename(file, 'others')
            destination = os.path.join(downloads_folder, 'others', new_name)
            try:
                shutil.move(file_path, destination)
                print(f"Moved {file} -> {destination}")
            except FileNotFoundError:
                print(f"Skipped {file} because it was not found or already deleted.")

# Main function to start the process
def main():
    print("Starting declutter process...")
    create_folders()
    move_files()
    print("Download folder is now organized!")

if __name__ == '__main__':
    main()
