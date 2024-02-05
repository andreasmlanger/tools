"""
Converts an epub file to awz3 and extracts the cover
All epub files need to be located in the 'Downloads' directory
Calibre needs to be installed
"""


import os
import sys
import re
import zipfile
import subprocess
from io import BytesIO
from PIL import Image

EBOOK_CONVERT = r'C:\Program Files\Calibre2\ebook-convert.exe'  # path to Calibre's ebook-convert.exe


class Ebook:
    @staticmethod
    def convert():
        path = os.environ['USERPROFILE'] + '\\Downloads\\'
        ebooks = [file for file in os.listdir(path) if file.endswith('.epub')]
        if len(ebooks) == 0:
            sys.exit('No epub files in Downloads directory.')
        for ebook in ebooks:
            print('\033[94m' + 'Converting: ' + ebook + '\033[90m')
            subprocess.call([EBOOK_CONVERT, path + ebook, path + ebook[:-5] + '.azw3'])
            Ebook.extract_cover(path, ebook)
        print('\033[36m' + 'Ebooks converted!')

    @staticmethod
    def extract_cover(path, ebook):
        print('\033[94m' + 'Extracting cover')
        file = open(path + ebook, 'rb')
        content = zipfile.ZipFile(BytesIO(file.read()), 'r')
        cover_regex = re.compile(r'.*cover.*\.(jpg|jpeg|png)', flags=re.IGNORECASE)
        for data in content.filelist:
            if cover_regex.match(data.filename):
                cover = content.open(data.filename)
                im = Image.open(BytesIO(cover.read()))
                im.save(path + ebook[:-5] + '.jpg', 'JPEG')
                return


def main():
    Ebook.convert()


if __name__ == '__main__':
    main()
