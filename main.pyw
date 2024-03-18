import os
import shutil
import datetime
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class NewFileHandler(FileSystemEventHandler):
    def on_create(self, event):
        if event.is_directory:
            return
        else:
            source_path = event.src_path
            filename = os.path.basename(source_path)
            today = datetime.datetime.now().strftime("%d.%m.%Y")
            destination_folder = os.path.join(os.getenv("SCANNED_FILES"), today)
            os.makedirs(destination_folder, exist_ok=True)
            destination_path = os.path.join(destination_folder, filename)
            shutil.move(source_path, destination_path)
            print(f"Moved {filename} to {destination_path}")

if __name__ == "__main__":
    folder_to_watch = os.getenv("SCANNED_FILES")
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=Flase)
    observer.start()
    print(f"Watching {folder_to_watch} for a new files...")

    try:
        while True:
            time.sleep(1)
    # except KeyboardInterrupt:
    #     observer.stop()
    #     observer.join()
