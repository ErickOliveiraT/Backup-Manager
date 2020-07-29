copy "C:\Users\erick\Desktop\Projetos\Backup Manager\src\check.py" "."
copy "C:\Users\erick\Desktop\Projetos\Backup Manager\src\compactor.py" "."
copy "C:\Users\erick\Desktop\Projetos\Backup Manager\src\credentials_drive.json" "."
copy "C:\Users\erick\Desktop\Projetos\Backup Manager\src\downloader.py" "."
copy "C:\Users\erick\Desktop\Projetos\Backup Manager\src\drive.py" "."
copy "C:\Users\erick\Desktop\Projetos\Backup Manager\src\filesHandler.py" "."
copy "C:\Users\erick\Desktop\Projetos\Backup Manager\src\interface.py" "."
copy "C:\Users\erick\Desktop\Projetos\Backup Manager\src\path.py" "."
copy "C:\Users\erick\Desktop\Projetos\Backup Manager\src\token.pickle" "."
python check.py -u
pause
del check.py
del compactor.py
del credentials_drive.json
del downloader.py
del drive.py
del filesHandler.py
del interface.py
del path.py
del token.pickle
exit