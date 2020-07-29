from datetime import datetime
import filesHandler
import json
import os

class Path_info():
    def __init__(self, folder_id):
        self.current_path = os.path.abspath(__file__)
        self.current_path = os.path.dirname(self.current_path)
        self.dirs = os.listdir(self.current_path)
        self.cloud_config = {
            "folder_id": folder_id,
            "local_path": self.current_path.replace('\\','/')
        }

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return round((total_size/1048576), 2)

def list_path(folder_id="FOLDER ID HERE"):
    path_info = Path_info(folder_id)
    folders = []
    for _dir in path_info.dirs:
        if _dir == 'path.py' or _dir == filesHandler.METADATA_FILE:
            continue
        checked_at = str(datetime.now()).split(' ')[0]
        abs_path = os.path.abspath(_dir)
        size = get_size(abs_path)
        folder_info = {
            "local_filename": _dir,
            "cloud_filename": _dir,
            "size": size,
            "checked_at": checked_at
        }
        folders.append(folder_info)
    data = {}
    data["cloud_config"] = path_info.cloud_config
    data["upload_info"] = folders
    filesHandler.save_metadata(data)