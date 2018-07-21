import os
import sys
from zipfile import ZipFile, ZIP_DEFLATED
import datetime
# import pathlib NEEDS TO BE MOVED FROM OS.PATH TO PATHLIB
from pathlib import Path


def getFiles(filePath, archivePath, fileName):

    # Can add more filtering with lambda or filter().
    # To move to recursive, use os.walk instead of os.listdir.
    for file in [file for file in Path(filePath).iterdir() if '.zip' not in file.name and file.is_file()]:
        #getctime may not work on linux.
        timeOfCreation = datetime.datetime.fromtimestamp(file.stat().st_mtime)
        archiveFile = '{}-{}_{}.zip'.format(timeOfCreation.year, timeOfCreation.month, fileName)

        #must list every time to account for new zip files.
        if Path(archivePath, archiveFile) in Path(archivePath).iterdir():
            with ZipFile(Path(archivePath, archiveFile), 'a', ZIP_DEFLATED) as zfile:
                zfile.write(file, file.name)
                print(file.name + ' Appended')
        else:
            with ZipFile(Path(archivePath, archiveFile), 'w', ZIP_DEFLATED) as zfile:
                zfile.write(file, file.name)
                print('Zip Created')

if __name__ == '__main__':
    assert len(sys.argv) == 4, 'Must pass in three paramaters. filePath, archivePath, fileName respectivly.'
    assert os.path.isdir(sys.argv[1]) and os.path.isdir(sys.argv[2]), 'Correct directories were not passed in'
    try:
        getFiles(filePath=sys.argv[1], archivePath=sys.argv[2], fileName=str(sys.argv[3]))
    except Exception as e:
        t = datetime.datetime.today()
        with open('{}-{}-{}-log.txt'.format(t.year, t.month, t.day), 'w') as f:
            f.write('paramaters: location of script: {}, filepath: {}, archivepath: {}, name: {}'.format(*sys.argv) +'\n')
            f.write('log failed with error: ' + '\n' + str(e))
        print('Error, check log file.')
