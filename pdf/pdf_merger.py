"""
Merges and optionally also rotates several pdf files
All files need to be copied into the 'Downloads' directory
"""

import os
import sys
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

PATH = os.path.join(os.environ['USERPROFILE'], 'Downloads')  # files go here


class PDF:
    @staticmethod
    def merge():
        pdf_files = [f for f in os.listdir(PATH) if f.endswith('.pdf')]
        if len(pdf_files) == 0:
            sys.exit('No PDF files in "Downloads" directory.')
        else:
            for pdf_file in pdf_files:
                print('\033[93m' + pdf_file + ' \033[94m' + 'was found')
            merger = PdfMerger()
            for f in pdf_files:
                merger.append(os.path.join(PATH, f))
            merged_file = os.path.join(PATH, 'merged_pdf.pdf')
            with open(merged_file, 'wb') as fh:
                merger.write(fh)
            print('\033[36m' + 'PDFs merged!')
            return merged_file

    @staticmethod
    def rotate(f):
        writer = PdfWriter()
        reader = PdfReader(f)
        for p in range(len(reader.pages)):
            page = reader.pages[p].rotate(90)
            writer.add_page(page)
        rotated_file = os.path.join(PATH, 'rotated_pdf.pdf')
        with open(rotated_file, 'wb') as fh:
            writer.write(fh)
        print('\033[36m' + 'PDF rotated!')


def main():
    f = PDF.merge()
    PDF.rotate(f)


if __name__ == '__main__':
    main()
