from datetime import datetime
import json
import os

METADATA_FILE = 'cloud_info.json'
current_path = os.path.abspath(__file__)
current_path = os.path.dirname(current_path)
dirs = os.listdir(current_path)

cloud_config = {
    "account": "erick.teixeira@unifei.edu.br",
    "folder_id": "14YigTgdUB9Qq8GYPue86Ddsm6hPn4HO7",
    "path": current_path.replace('\\','/').replace('D:','Disco D:')
}

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return round((total_size/1048576),2)

folders = []
for _dir in dirs:
    if _dir == 'list.py':
        continue
    checked_at = str(datetime.now()).split(' ')[0]
    _type = "folder"
    abs_path = os.path.abspath(_dir)
    size = get_size(abs_path)
    folder_info = {
        "type": _type,
        "local_filename": _dir,
        "cloud_filename": _dir,
        "size": size,
        "checked_at": checked_at
    }
    folders.append(folder_info)

data = {}
data["cloud_config"] = cloud_config
data["upload_info"] = folders
with open(METADATA_FILE, 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile)