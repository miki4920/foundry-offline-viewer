#!/usr/bin/python
import time
import os.path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from update_file import db, CreateDatabase


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        db.create_all()
        db.drop_all()
        db.create_all()
        CreateDatabase().insert_into_database(db)


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler,
                      path="C:/Users/Mikolaj Grobelny/AppData/Local/FoundryVTT/Data/worlds/darklands/data/",
                      recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
