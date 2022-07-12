from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from update_file import db, CreateDatabase


class FoundryHandler(FileSystemEventHandler):
    def __init__(self, path, file_name):
        self.file_name = file_name
        self.observer = Observer()
        self.observer.schedule(self, path, recursive=False)
        self.observer.start()
        self.observer.join()

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(self.file_name):
            db.create_all()
            db.drop_all()
            db.create_all()
            CreateDatabase().insert_into_database(db)


if __name__ == "__main__":
    event_handler = FoundryHandler("C:/Users/Mikolaj Grobelny/AppData/Local/FoundryVTT/Data/worlds/darklands/data/",
                                   "actors.db")
