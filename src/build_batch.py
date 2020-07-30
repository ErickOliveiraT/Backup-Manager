import sys

if len(sys.argv) > 1 and sys.argv[1].lower().split('-')[1] == 'windows':
    batch = open('check.bat', 'w')
else: sys.exit()

location = input('Installation Folder: ')
asp = chr(34)
files = [
    'check.py',
    'compactor.py',
    'credentials_drive.json',
    'drive.py',
    'filesHandler.py',
    'interface.py',
    'path.py',
    'token.pickle'
]

for file in files:
    batch.write('copy ' + asp + location + '\\' + file + asp + ' ' + asp + '.' + asp + '\n')
batch.write('cls\n')
batch.write('python check.py -u\n')
batch.write('pause\n')
for file in files:
    batch.write('del ' + file + '\n')
batch.write('exit')
batch.close()