from datetime import datetime
import filesHandler
import drive
import json

metadata = filesHandler.load_metadata()
folder_id = metadata["cloud_config"]["folder_id"]
itens = metadata["upload_info"]

def get_filenames(files):
    filenames = []
    for file in files:
        filenames.append(file["name"].split('.')[0])
    return filenames

cloud_files = drive.get_files(folder_id)
cloud_filenames = get_filenames(cloud_files)

def get_file_id(filename):
    for file in cloud_files:
        if file["name"].split('.')[0] == filename:
            return file["id"]
    return False

missing = False
file_index = 0
for item in itens:
    checked_at = str(datetime.now()).split(' ')[0]
    metadata["upload_info"][file_index]["checked_at"] = checked_at
    filename = item["cloud_filename"]
    if not filename in cloud_filenames:
        missing = True
        print('Missing', item["local_filename"])
    else:
        file_id = get_file_id(filename)
        metadata["upload_info"][file_index]["file_id"] = file_id
    file_index += 1
filesHandler.update_metadata(metadata)
if not missing:
    print('All files are backed up!')