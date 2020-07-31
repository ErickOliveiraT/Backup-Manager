from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaIoBaseDownload
from apiclient.http import MediaFileUpload
import filesHandler
import requests
import os.path
import pickle
import io

class Config:
  def __init__(self, first_login=False):
    self.SCOPES = ['https://www.googleapis.com/auth/drive']
    if first_login: self.PATH_ID = filesHandler.get_folder_id()
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
    media = MediaFileUpload(filename, mimetype='application/zip')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('Upload done')
    return file.get('id')

def upload(filename):
    config = Config()
    fileID = handleUpload(filename, config)
    if fileID and config.DELETE_AFTER_UPLOAD:
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