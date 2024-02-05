"""
Cleans up mp3 collection on Google Drive and updates ID3 tags from file names
"""

from PIL import Image
from mutagen.id3 import ID3, TIT2, TRCK, TALB, TPE1, TPE2, APIC, TDRC, ID3NoHeaderError
import os
import sys
import datetime


LIBRARY = 'G:\\My Drive\\Music'  # path of music files


class Mp3:
    @staticmethod
    def analyze():
        folders = [x[0] for x in os.walk(LIBRARY)][1:]
        for folder in folders:
            albums, songs = set(), set()
            for file in os.listdir(folder):
                if file.endswith('.jpg'):
                    number = file.split(' - ')[1]
                    if number in albums:
                        sys.exit('\033[91m' + 'Duplicate album number\n' + '\033[92m' + folder)
                    albums.add(number)
                    album_art = Image.open(folder + '\\' + file)
                    if album_art.size[0] < 500 or album_art.size[1] < 500:
                        sys.exit('\033[91m' + 'Too small album art\n' + '\033[92m' + folder + '\\' + file)
                elif file.endswith('.mp3'):
                    number = file.split(' - ')[1]
                    if number in songs:
                        sys.exit('\033[91m' + 'Duplicate song number\n' + '\033[92m' + folder)
                    songs.add(number)
                elif '.' in file:
                    sys.exit('\033[91m' + 'Not a jpg or mp3 file\n' + '\033[92m' + folder)
            if albums and max([int(item[0]) for item in albums]) > len(albums):
                sys.exit('\033[91m' + 'Missing album number\n' + '\033[92m' + folder)
            if any([item[-3:] != 'x00' for item in albums]):
                sys.exit('\033[91m' + 'Incorrect album art numbering\n' + '\033[92m' + folder)
            if songs and max([int(item[0]) for item in songs]) > len(set([item[0] for item in songs])):
                sys.exit('\033[91m' + 'Incorrect song numbering\n' + '\033[92m' + folder)
            if set([item[0] for item in albums]) != set([item[0] for item in songs]):
                sys.exit('\033[91m' + 'Missing song or album art\n' + '\033[92m' + folder)
        print('\033[36m' + 'No errors found!')

    @staticmethod
    def update_id3_tags():
        print('\033[94m' + 'Press ENTER to start updating ID3 tags')
        input()
        folders = [x[0] for x in os.walk(LIBRARY)][1:]
        for folder in folders:
            cover, album, artist = None, None, None
            for file in os.listdir(folder):
                if file.endswith('.jpg'):
                    cover = folder + '\\' + file
                    album = file.split(' - ')[2][:-4]  # remove '.jpg' from album name
                    artist = file.split(' - ')[0]
                elif file.endswith('.mp3'):
                    title = file.split(' - ')[2][:-4]  # remove '.mp3' from title name
                    number = file.split(' - ')[1][-2:]
                    try:
                        tags = ID3(folder + '\\' + file)
                        year = str(tags['TDRC'])  # save year information if available
                        tags.delete()
                    except (ID3NoHeaderError, KeyError):
                        tags = ID3()
                        year = str(datetime.datetime.now().year)
                    with open(cover, 'rb') as album_art:
                        tags['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=album_art.read())
                    tags['TPE1'] = TPE1(encoding=3, text=artist)  # contributing artist
                    tags['TPE2'] = TPE2(encoding=3, text=artist)  # album artist
                    tags['TIT2'] = TIT2(encoding=3, text=title)   # title
                    tags['TALB'] = TALB(encoding=3, text=album)   # album
                    tags['TDRC'] = TDRC(encoding=3, text=year)    # year
                    tags['TRCK'] = TRCK(encoding=3, text=number)  # track number
                    tags.save(folder + '\\' + file)
                    print('\033[92m' + file)
        print('\033[36m' + 'All ID3 tags updated!')


def main():
    Mp3.analyze()
    Mp3.update_id3_tags()


if __name__ == '__main__':
    main()
