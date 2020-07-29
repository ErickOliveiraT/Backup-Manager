import zipfile
import os

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