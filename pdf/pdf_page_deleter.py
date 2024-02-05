"""
Delete pages from pdf file
The file must be copied into the 'Downloads' directory
"""

import os
import sys
from PyPDF2 import PdfReader, PdfWriter

PATH = os.path.join(os.environ['USERPROFILE'], 'Downloads')  # file goes here


class PDF:
    @staticmethod
    def delete():
        pdf_files = [f for f in os.listdir(PATH) if f.endswith('.pdf')]
        if len(pdf_files) == 0:
            sys.exit('No PDF file in "Downloads" directory.')
        elif len(pdf_files) > 1:
            sys.exit('More than one PDF file found.')
        else:
            pdf_file = pdf_files[0]
            print('\033[93m' + pdf_file + ' \033[94m' + 'was found\nEnter pages to delete, e.g. 1,4-6,9')
            numbers = input()
            try:
                pages_to_delete = []
                for block in numbers.split(','):
                    if '-' in block:
                        start, end = map(int, block.split('-'))
                        pages_to_delete.extend(range(start - 1, end))
                    else:
                        pages_to_delete.append(int(block) - 1)
                reader = PdfReader(os.path.join(PATH, pdf_file))
                writer = PdfWriter()

                for p in range(len(reader.pages)):
                    if p not in pages_to_delete:
                        page = reader.pages[p]
                        writer.add_page(page)

                new_pdf_file = os.path.splitext(os.path.join(PATH, pdf_file))[0] + '_deleted.pdf'
                with open(new_pdf_file, 'wb') as fh:
                    writer.write(fh)

                print('\033[94m' + 'Deleting complete!')
            except ValueError:
                print('\033[91m' + 'No pages selected')


def main():
    PDF.delete()


if __name__ == '__main__':
    main()
