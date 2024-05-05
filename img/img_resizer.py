"""
Resizes images to specified width W and height H (images will be overwritten!)
The files need to be located in the 'Downloads' directory
"""

from PIL import Image
import os
import sys

W = 1000
# H = 1500
H = 1000

PATH = os.path.join(os.environ['USERPROFILE'], 'Downloads')  # files go here


class Images:
    @staticmethod
    def resize():
        try:
            files = [f for f in os.listdir(PATH) if f.endswith('.jpg') or f.endswith('.png')]
        except FileNotFoundError:
            sys.exit("No images found in 'Downloads' directory")
        for file in files:
            im = Image.open(os.path.join(PATH, file))
            w, h = im.size
            if w == W and h == H:
                continue
            print('\033[93m' + file + ' \033[94m' + 'was found')
            im = im.resize((W, H))
            im.save(os.path.join(PATH, file), optimize=True)
        print('\033[36m' + 'All images resized!')


def main():
    Images.resize()


if __name__ == '__main__':
    main()
