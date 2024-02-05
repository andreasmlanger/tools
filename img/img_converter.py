"""
Converts for example PNG images to TIFF
The files need to be copied into the 'Downloads' directory
"""

from PIL import Image
import os
import sys

OLD = 'png'
NEW = 'tiff'

PATH = os.path.join(os.environ['USERPROFILE'], 'Downloads')  # files go here


class Images:
    @staticmethod
    def convert():
        files = [f for f in os.listdir(PATH) if f.endswith(f'.{OLD}')]
        if len(files) == 0:
            sys.exit(f"No {OLD} files in 'Downloads' directory!")
        for file in files:
            print('\033[93m' + file + ' \033[94m' + 'was found')
            im = Image.open(os.path.join(PATH, file))
            im.save(os.path.join(PATH, file).replace(f'.{OLD}', f'.{NEW}'), optimize=True)
        print('\033[36m' + 'All images converted!')


def main():
    Images.convert()


if __name__ == '__main__':
    main()
