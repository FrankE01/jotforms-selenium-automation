import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
import shutil
import re


path = "C:\\FRANCIS_ECHESI\\playground\\automation\\files"
submission_files = {}
next_two = []


class DownloadHandler(FileSystemEventHandler):
    def on_moved(self, event):

        if event.is_directory == False:
            file_path = event.dest_path
            f, ext = os.path.splitext(file_path)
            # print(ext)
            if ext == ".crdownload" or ext == ".": 
                return
            file_name = os.path.basename(file_path)
            submission_name = ""

            if len(next_two) < 1:
                next_two.append(file_path)
            else:
                next_two.append(file_path)
                for name in next_two:
                    if bool(re.match('^[0-9]+$', os.path.basename(name))):
                        submission_name = os.path.basename(name)
                        f, ext = os.path.splitext(submission_name)
                        submission_name = f
                    else:
                        submission_name = os.path.basename(next_two[1])
                        f, ext = os.path.splitext(submission_name)
                        submission_name = f

                submission_files[submission_name]=[next_two[0], next_two[1]]
                next_two.pop()
                next_two.pop()
            
                print(submission_files[submission_name])
                print(submission_name)
                submission_folder = os.path.join(os.path.dirname(file_path), submission_name)
                if not os.path.exists(submission_folder):
                    os.makedirs(submission_folder)
                for file_to_move in submission_files[submission_name]:
                    if not os.path.exists(os.path.join(submission_folder, os.path.basename(file_to_move))):
                        shutil.move(file_to_move, submission_folder)
                        

                submission_files[submission_name] = submission_files[submission_name][-2:]
            

if __name__ == "__main__":
    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()