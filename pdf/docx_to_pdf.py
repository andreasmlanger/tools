"""
Converts several docx files to pdf
All files need to be copied into the 'Downloads' directory
"""

from docx2pdf import convert
import os
import sys

PATH = os.path.join(os.environ['USERPROFILE'], 'Downloads')  # files go here


class DOCX:
    @staticmethod
    def convert_to_pdf():
        files = [f for f in os.listdir(PATH) if f.endswith('.docx') and '~' not in f]
        if len(files) == 0:
            sys.exit('No DOCX files in "Downloads" directory.')
        else:
            for f in files:
                print('\033[93m' + f)
                convert(os.path.join(PATH, f))
            print('\033[36m' + 'All DOCX files converted to PDF!')


def main():
    DOCX.convert_to_pdf()


if __name__ == '__main__':
    main()
