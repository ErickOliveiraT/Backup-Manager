import filesHandler
import interface
import drive
import sys

try:
    metadata = filesHandler.load_metadata()
except Exception as error:
    str_error = str(type(error))
    if str_error.find('FileNotFoundError') != -1:
        print('{} file not found.'.format(filesHandler.METADATA_FILE))
        print('You have to check this folder before downloading any data')
        sys.exit()

def get_file_list(metadata):
    itens = metadata["upload_info"]
    file_list = []
    for item in itens:
        if item["file_id"]:
            file_list.append(item["cloud_filename"])
    return file_list

def get_file_id(filename):
    itens = metadata["upload_info"]
    for item in itens:
        if item["cloud_filename"] == filename:
            return item["file_id"]
    return False

file_list = get_file_list(metadata)
choices = interface.show_download_options(file_list)
if choices == None:
    sys.exit()
for item in choices:
    filename = file_list[item]
    file_id = get_file_id(filename)
    print('\nDownloading {}'.format(filename))
    drive.download(file_id)
    break