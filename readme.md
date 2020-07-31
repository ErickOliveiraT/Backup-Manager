# Backup-Manager

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Backup-Manager is a free open source to sync a folder with Google Drive. It works by searching all not uploaded subfolders of a folder, compressing it and uploading to the cloud. 

## Features

  - Compression [OK]
  - Upload [OK]
  - Download [Future]

## Installation

### Step 1: Install Dependencies
 Run this command:
```sh
$ pip install -r requirements.txt
```

### Step 2: Enable Google Drive API
##### Access: https://developers.google.com/drive/api/v3/quickstart/python
##
![enable](https://raw.githubusercontent.com/ErickOliveiraT/Backup-Manager/master/images/enable.png)
##### Warning: This filename must be 'credentials_drive.json' not 'credentials.json' (as default)
##

### Step 3: Login to your Google Drive Account:
 Run this command:
```sh
$ python src/login.py
```

### Step 4: Copy all files in /src to a definitive folder:
 That's the folder we'll call when executing the program.
 For example: C:\Program Files\Backup Manager

### Step 5: Generate a Batch File:
 Run this command (for Windows):
```sh
$ python build_batch.py -windows
```

##### Save the generated 'check.bat' file for later.
#
#
## First Run

### Step 1: Copy the 'check.bat' file to the folder you wanna sync:
![Run1](https://raw.githubusercontent.com/ErickOliveiraT/Backup-Manager/master/images/run_1.PNG)

### Step 2: Get the ID of your Google Drive Folder:
![Run2](https://raw.githubusercontent.com/ErickOliveiraT/Backup-Manager/master/images/run_2.png)

### Step 3: Run 'check.bat' the insert your ID from Step 2:
![Run3](https://raw.githubusercontent.com/ErickOliveiraT/Backup-Manager/master/images/run_3.png)

### If you have non uploaded files, you'll see this:
![miss](https://raw.githubusercontent.com/ErickOliveiraT/Backup-Manager/master/images/missing.PNG)

### And you can upload missing itens by choosing between the options:
![upload](https://raw.githubusercontent.com/ErickOliveiraT/Backup-Manager/master/images/uploading.PNG)

### If all the files are uploaded, you'll see this message:
![ok](https://raw.githubusercontent.com/ErickOliveiraT/Backup-Manager/master/images/ok.PNG)