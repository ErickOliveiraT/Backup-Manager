from datetime import datetime
import filesHandler
import interface
import drive
import json
import path
import sys

try:
    metadata = filesHandler.load_metadata()
except Exception as error:
    str_error = str(type(error))
    if str_error.find('FileNotFoundError') != -1:
        print('{} file not found.'.format(filesHandler.METADATA_FILE))
        folder_id = input('\nInsert Google Drive Folder ID: ')
        path.list_path(folder_id)
        print('')
        metadata = filesHandler.load_metadata()
        sys.argv.clear()

folder_id = metadata["cloud_config"]["folder_id"]

if len(sys.argv) > 1:
    if sys.argv[1] == '-update' or sys.argv[1] == '-u':
        path.list_path(folder_id)
        metadata = filesHandler.load_metadata()

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

missing_itens = []
missing = False
file_index = 0
for item in itens:
    checked_at = str(datetime.now()).split(' ')[0]
    metadata["upload_info"][file_index]["checked_at"] = checked_at
    filename = item["cloud_filename"].split('.')[0]
    if not filename in cloud_filenames:
        missing = True
        missing_itens.append(item["local_filename"])
        print('Missing', item["local_filename"])
    else:
        file_id = get_file_id(filename)
        metadata["upload_info"][file_index]["file_id"] = file_id
    file_index += 1
filesHandler.save_metadata(metadata)
if not missing:
    print('All files are backed up!')
else:
    interface.show_upload_options(missing_itens)