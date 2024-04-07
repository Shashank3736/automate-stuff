import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
import datetime

# Define all file types in json format
FILE_TYPES = {
    'Documents': ['.pdf', '.csv', '.docx', '.xlsx', '.pptx', '.doc', '.xls', '.ppt', '.txt', '.epub'],
    'Pictures': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.heic', '.heif'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
    'Music': ['.mp3', '.wav', '.ogg', '.aac', '.flac', '.wma', '.ape', '.aiff', '.alac'],
    'Compressed': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.tgz', '.rpm', '.deb'],
    'Apps': ['.exe', '.dmg', '.pkg', '.deb', '.rpm', '.app', '.msi', '.appx', '.appxbundle'],
}

LOGS_FOLDER = "F:/automate-stuff/logs"

def log(message: str):
    """
    Save logs in a file downloads_file.log in this folder
    """
    # Check if folder exist or not. If not create one.
    if not os.path.exists(f'{LOGS_FOLDER}/{datetime.datetime.today().strftime("%Y-%m-%d")}'):
        os.makedirs(f'{LOGS_FOLDER}/{datetime.datetime.today().strftime("%Y-%m-%d")}')
    
    # Open or create and open file and add the logs
    with open(f'{LOGS_FOLDER}/{datetime.datetime.today().strftime("%Y-%m-%d")}/download_file.log', 'a') as f:
        f.write(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {message}\n")
    
    # print the logs in terminal
    print(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {message}")


class FileHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        # Check all the files and replace if they are .pdf or .csv
        # for root, dirs, files in os.walk(os.path.expanduser('~') + '/Downloads'):
        for file in os.listdir(os.path.expanduser('~') + '/Downloads'):
            # check if the it is a file or directory
            if os.path.isdir(os.path.join(os.path.expanduser('~'), 'Downloads', file)):
                continue
            # Get the file extension
            _, ext = os.path.splitext(file)
            dest_folder = None
            if ext.lower() in FILE_TYPES['Documents']:
                dest_folder = os.path.join(os.path.expanduser('~'), 'Documents', 'Downloads', ext.lower()[1:])
            elif ext.lower() in FILE_TYPES['Pictures']:
                dest_folder = os.path.join(os.path.expanduser('~'), 'Pictures', 'Downloads')
            elif ext.lower() in FILE_TYPES['Videos']:
                dest_folder = os.path.join(os.path.expanduser('~'), 'Videos', 'Downloads')
            elif ext.lower() in FILE_TYPES['Music']:
                dest_folder = os.path.join(os.path.expanduser('~'), 'Music', 'Downloads')
            elif ext.lower() in FILE_TYPES['Compressed']:
                dest_folder = os.path.join(os.path.expanduser('~'), 'Documents', 'Downloads', 'Compressed')
            src_path = os.path.join(os.path.expanduser('~'), 'Downloads', file)
            if src_path and dest_folder:
                # Does dest_folder exist?
                if not os.path.exists(dest_folder):
                    log(f"Creating {dest_folder}")
                    os.makedirs(dest_folder)
                dest_path = os.path.join(dest_folder, file)
                log(f"Replacing {src_path} with {dest_path}")
                shutil.move(src_path, dest_path)
                log(f"Moved {src_path} to {dest_path}")
    def on_created(self, event):
        if os.path.isdir(event.src_path):
            return
        log(f"File {event.src_path} created.")
        # Get the file extension
        _, ext = os.path.splitext(event.src_path)

        # Define the destination folder based on the extension
        if ext.lower() in FILE_TYPES['Documents']:
            dest_folder = os.path.join(os.path.expanduser('~'), 'Documents', 'Downloads', ext.lower()[1:])
        elif ext.lower() in FILE_TYPES['Pictures']:
            dest_folder = os.path.join(os.path.expanduser('~'), 'Pictures', 'Downloads')
        elif ext.lower() in FILE_TYPES['Videos']:
            dest_folder = os.path.join(os.path.expanduser('~'), 'Videos', 'Downloads')
        elif ext.lower() in FILE_TYPES['Music']:
            dest_folder = os.path.join(os.path.expanduser('~'), 'Music', 'Downloads')
        elif ext.lower() in FILE_TYPES['Compressed']:
            dest_folder = os.path.join(os.path.expanduser('~'), 'Documents', 'Downloads', 'Compressed')
        else:
            return
        # check if 'Downloads' folder exists if not create one
        log(f"Checking {dest_folder}")
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        # Move the file to the destination folder
        try:
            dest_path = os.path.join(dest_folder, os.path.basename(event.src_path))
            shutil.move(event.src_path, dest_path)
            log(f"Moved {event.src_path} to {dest_path}")
        except Exception as e:
            log(f"Error moving {event.src_path}: {e}")
    
    def on_modified(self, event: FileSystemEvent) -> None:
        # super().on_modified(event)
        log(f"File {event.src_path} modified.")
        # check if after modification file exist or not
        if not os.path.exists(event.src_path):
            log(f"File {event.src_path} deleted.")
            return
        return self.on_created(event)

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