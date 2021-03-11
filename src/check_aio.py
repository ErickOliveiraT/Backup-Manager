from __future__ import print_function
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from apiclient.http import MediaFileUpload

from datetime import datetime

import mimetypes
import requests
import os.path
import zipfile
import pickle
import json
import sys
import os
import io

METADATA_FILE = 'cloud_info.json'

class Path_info():
    def __init__(self, folder_id):
        self.current_path = os.path.abspath(__file__)
        self.current_path = os.path.dirname(self.current_path)
        self.dirs = os.listdir(self.current_path)
        self.cloud_config = {
            "folder_id": folder_id,
            "local_path": self.current_path.replace('\\','/')
        }
        self.ignore_list = [
            'check.bat',
            'check.py',
            'compactor.py',
            'credentials_drive.json',
            'downloader.py',
            'drive.py',
            'filesHandler.py',
            'path.py',
            'interface.py',
            'token.pickle',
            '__pycache__',
            'build_batch.py',
            'login.py',
            'setup.py',
            'check_aio.py'
        ]

class Config:
    def __init__(self, first_login=False):
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        if not first_login:
            self.PATH_ID = get_folder_id()
        self.DELETE_AFTER_UPLOAD = True

def load_credentials(config):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials_drive.json', config.SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service

def handleUpload(filename, config):
    print('Uploading {}'.format(filename))
    file_metadata = {'name': filename, 'parents': [config.PATH_ID]}
    drive_service = load_credentials(config)
    mime_type = getMIMEType(filename)
    media = MediaFileUpload(filename, mimetype=mime_type)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('Upload done')
    return file.get('id')

def upload(filename, auto_generated=False):
    config = Config()
    fileID = handleUpload(filename, config)
    if fileID and config.DELETE_AFTER_UPLOAD and auto_generated:
        os.remove(filename)

def get_files(parent):
    config = Config()
    drive_service = load_credentials(config)
    page_token = None
    files = []
    while True:
        response = drive_service.files().list(q="'{}' in parents".format(parent),
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name, parents)',
                                            pageToken=page_token).execute()
        for file in response.get('files', []):
            files.append(file)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files

def download(file_id):
    config = Config()
    drive_service = load_credentials(config)
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

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
        if _dir in path_info.ignore_list or _dir == METADATA_FILE:
            continue
        checked_at = str(datetime.now()).split(' ')[0]
        abs_path = os.path.abspath(_dir)
        size = get_size(abs_path)
        _type = 'folder'
        if _dir.find('.') != -1: _type = 'file'
        folder_info = {
            "type": _type,
            "local_filename": _dir,
            "cloud_filename": _dir,
            "size": size,
            "checked_at": checked_at
        }
        folders.append(folder_info)
    data = {}
    data["cloud_config"] = path_info.cloud_config
    data["upload_info"] = folders
    save_metadata(data)

def load_metadata():
    with open(METADATA_FILE, encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data

def get_folder_id():
    metadata = load_metadata()
    cloud_config = metadata["cloud_config"]
    return cloud_config["folder_id"]

def get_cloud_metadata():
    metadata = load_metadata()
    return metadata["cloud_config"]

def save_metadata(metadata):
    with open(METADATA_FILE, 'w', encoding='utf-8') as outfile:
        json.dump(metadata, outfile)

def getMIMEType(filename):
    return mimetypes.MimeTypes().guess_type(filename)[0]

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def build_zip(path, filename=''):
    if filename == '':
        filename = path.split('./')[1].split('.')[0]
    if filename.find('.zip') == -1:
        filename += '.zip'
    zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    if path[len(path)-1] != '/':
        path += '/'
    zipdir(path, zipf)
    zipf.close()
    return filename

try:
    metadata = load_metadata()
except Exception as error:
    str_error = str(type(error))
    if str_error.find('FileNotFoundError') != -1:
        print('{} file not found.'.format(METADATA_FILE))
        folder_id = input('\nInsert Google Drive Folder ID: ')
        list_path(folder_id)
        print('')
        metadata = load_metadata()
        sys.argv.clear()

folder_id = metadata["cloud_config"]["folder_id"]

if len(sys.argv) > 1:
    if sys.argv[1] == '-update' or sys.argv[1] == '-u':
        list_path(folder_id)
        metadata = load_metadata()

itens = metadata["upload_info"]

def get_filenames(files):
    filenames = []
    for file in files:
        filenames.append(file["name"].split('.')[0])
    return filenames

cloud_files = get_files(folder_id)
cloud_filenames = get_filenames(cloud_files)

def get_file_id(filename):
    for file in cloud_files:
        if file["name"].split('.')[0] == filename:
            return file["id"]
    return False

def show_upload_options(itens):
    print('\nDo you want to upload any item?\n')
    print('[0] No')
    for i in range(0,len(itens)):
        print('[{}] {}'.format(i+1,itens[i]))
    print('[{}] All'.format(len(itens)+1))
    choice = input('\nOption: ')
    if choice == '0': #None
        sys.exit()
    if choice.find(',') == -1 and int(choice) == len(itens)+1: #All
        index = 1
        for item in itens:
            print('\n{} of {}'.format(index,len(itens)))
            if item.find('.') != -1: #is file
                upload(item)
            else: #is folder
                path = './' + item          
                print('Compressing {}'.format(item))
                zip_file = build_zip(path)
                upload(zip_file, True)
            index += 1
        sys.exit()
    #Custom
    choices = choice.split(',')
    index = 1
    for i in range(0,len(choices)):
        print('\n{} of {}'.format(index,len(choices)))
        if itens[int(choices[i])-1].find('.') != -1: #is file
            upload(itens[int(choices[i])-1])
        else:
            path = './' + itens[int(choices[i])-1]
            print('Compressing {}'.format(itens[int(choices[i])-1]))
            zip_file = build_zip(path)
            upload(zip_file, True)
        index += 1
    sys.exit()

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
save_metadata(metadata)
if not missing:
    print('All files are backed up!')
else:
    show_upload_options(missing_itens)