import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from common.model import dynamodb
from client_side.update_file import CreateDatabase


class FoundryHandler(FileSystemEventHandler):
    def __init__(self):
        path = os.getenv("FOUNDRY_PATH").split("/")
        self.file_name = path[-1:][0]
        self.observer = Observer()
        self.observer.event_queue.maxsize = 100
        self.observer.schedule(self, "/".join(path[:-1]), recursive=False)
        self.observer.start()
        self.observer.join()

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(self.file_name):
            CreateDatabase(dynamodb).insert_into_database()


if __name__ == "__main__":
    FoundryHandler()
