"""
Converts an epub file into an audiobook mp3
All epub files need to be located in the 'Downloads' directory
Modify FIRST_CHAPTER parameter if required
Google API allows a max of 50 requests per day
"""

from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
from gtts import gTTS
import os
import sys


PATH = os.environ['USERPROFILE'] + '\\Downloads\\'  # files go here
BLACKLIST = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script', 'style']
FIRST_CHAPTER = 0


class Ebook:
    @staticmethod
    def convert():
        ebooks = [file for file in os.listdir(PATH) if file.endswith('.epub')]
        if len(ebooks) == 0:
            sys.exit('No epub files in Downloads directory.')
        for ebook in ebooks:
            ebook_title = ebook[:-5]

            print('\033[94m' + 'Converting: ' + ebook + '\033[90m')
            try:
                chapters = Ebook.epub2text(PATH + ebook)  # split epub into chapters with text strings
                print(f'{len(chapters)} chapters found.')

                for idx, chapter in enumerate(chapters):
                    if idx > FIRST_CHAPTER - 2:
                        Ebook.text2mp3(chapter, idx + 1, ebook_title)
            except Exception as ex:
                sys.exit(str(ex))
        print('\033[36m' + 'Ebooks converted!')

    @staticmethod
    def epub2text(epub_path):
        html_chapters = Ebook.epub2html(epub_path)
        text_chapters = Ebook.html2text(html_chapters)
        return text_chapters

    @staticmethod
    def epub2html(epub_path):
        book = epub.read_epub(epub_path)
        chapters = []
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                chapters.append(item.get_content())
        return chapters

    @staticmethod
    def html2text(html_chapters):
        chapters = []
        for html in html_chapters:
            output = ''
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.find_all(string=True)
            for t in text:
                if t.parent.name not in BLACKLIST:
                    output += '{} '.format(t)
            output = Ebook.clean_text(output)
            if len(output) > 2000:  # minimum character number per chapter
                chapters.append(output)
        return chapters

    @staticmethod
    def clean_text(text):
        word_list = text.split()  # split all words into list and remove whitespaces
        for idx, word in enumerate(word_list):
            if word[1:] != word.lower()[1:]:  # check if word is all uppercase
                word_list[idx] = word_list[idx].capitalize()
        text = ' '.join(word_list)
        text = text.lstrip('0123456789.- ')  # remove leading digits, e.g. from chapters
        return text

    @staticmethod
    def text2mp3(text, idx, title):
        file_name = os.path.join(PATH, title + '_{:03d}'.format(idx) + '.mp3')
        print(f'Converting {file_name}')
        speech = gTTS(text=text, lang='en', slow=False)
        speech.save(file_name)


def main():
    Ebook.convert()


if __name__ == '__main__':
    main()
