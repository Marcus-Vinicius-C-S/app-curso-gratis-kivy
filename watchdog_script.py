import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import Popen

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None
        self.start_process()

    def start_process(self):
        if self.process:
            self.process.kill()
        self.process = Popen(self.command, shell=True)

    def on_any_event(self, event):
        if event.src_path.endswith('.py') or event.src_path.endswith('.kv'):
            self.start_process()

if __name__ == "__main__":
    path = "."
    command = "python main.py"
    event_handler = FileChangeHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
