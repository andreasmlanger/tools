"""
Crops images to a specified SIZE (images will be overwritten!)
The files need to be located in the 'Downloads' directory
"""

from PIL import Image
import os
import sys

BOX = 162, 268, 1000, 1000  # left, upper, right, lower pixel
SIZE = 500, 500

PATH = os.path.join(os.environ['USERPROFILE'], 'Downloads')  # files go here


class Images:
    @staticmethod
    def crop():
        files = [f for f in os.listdir(PATH) if f.endswith('.jpg') or f.endswith('.png')]
        if len(files) == 0:
            sys.exit("No images found in 'Downloads' directory")
        for file in files:
            print('\033[93m' + file + ' \033[94m' + 'was found')
            im = Image.open(os.path.join(PATH, file))
            im = im.crop(BOX)
            im = im.resize(SIZE)
            im.save(os.path.join(PATH, file), optimize=True)

        print('\033[36m' + 'All images cropped!')


def main():
    Images.crop()


if __name__ == '__main__':
    main()
