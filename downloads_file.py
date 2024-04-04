import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define all file types in json format
FILE_TYPES = {
    'Documents': ['.pdf', '.csv', '.docx', '.xlsx', '.pptx', '.doc', '.xls', '.ppt', '.txt', '.epub'],
    'Pictures': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.heic', '.heif'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
    'Music': ['.mp3', '.wav', '.ogg', '.aac', '.flac', '.wma', '.ape', '.aiff', '.alac'],
    'Compressed': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.tgz', '.rpm', '.deb'],
    'Apps': ['.exe', '.dmg', '.pkg', '.deb', '.rpm', '.app', '.msi', '.appx', '.appxbundle'],
}

class FileHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        # Check all the files and replace if they are .pdf or .csv
        for root, dirs, files in os.walk(os.path.expanduser('~') + '/Downloads'):
            for file in files:
                _, ext = os.path.splitext(file)
                src_path, dest_path = None, None
                if ext.lower() in FILE_TYPES['Documents']:
                    src_path = os.path.join(root, file)
                    dest_path = os.path.join(os.path.expanduser('~'), 'Documents', 'Downloads', file)
                elif ext.lower() in FILE_TYPES['Pictures']:
                    src_path = os.path.join(root, file)
                    dest_path = os.path.join(os.path.expanduser('~'), 'Pictures', 'Downloads', file)
                elif ext.lower() in FILE_TYPES['Videos']:
                    src_path = os.path.join(root, file)
                    dest_path = os.path.join(os.path.expanduser('~'), 'Videos', 'Downloads', file)
                elif ext.lower() in FILE_TYPES['Music']:
                    src_path = os.path.join(root, file)
                    dest_path = os.path.join(os.path.expanduser('~'), 'Music', 'Downloads', file)
                if src_path and dest_path:
                    print(f"Replacing {src_path} with {dest_path}")
                    shutil.move(src_path, dest_path)
                    print(f"Moved {src_path} to {dest_path}")
    def on_created(self, event):
        print(f"File {event.src_path} created.")
        # Get the file extension
        _, ext = os.path.splitext(event.src_path)

        # Define the destination folder based on the extension
        if ext.lower() in ['.pdf', '.csv']:
            dest_folder = os.path.join(os.path.expanduser('~'), 'Documents')
        else:
            # Add more extensions and destinations as needed
            return

        # Move the file to the destination folder
        dest_path = os.path.join(dest_folder, os.path.basename(event.src_path))
        shutil.move(event.src_path, dest_path)
        print(f"Moved {event.src_path} to {dest_path}")

if __name__ == "__main__":
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, downloads_folder, recursive=False)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()