import os
import requests

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from common.model import db
from update_file import CreateDatabase


def send_database():
    with open('../wealth.db', 'rb') as file:
        requests.post(os.getenv("URL"), data=file)


class FoundryHandler(FileSystemEventHandler):
    def __init__(self):
        path = os.getenv("FOUNDRY_PATH").split("/")
        self.file_name = path[-1:][0]
        self.observer = Observer()
        self.observer.schedule(self, "/".join(path[:-1]), recursive=False)
        self.observer.start()
        self.observer.join()

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(self.file_name):
            db.create_all()
            db.drop_all()
            db.create_all()
            CreateDatabase().insert_into_database(db)
            send_database()


if __name__ == "__main__":
    event_handler = FoundryHandler()
