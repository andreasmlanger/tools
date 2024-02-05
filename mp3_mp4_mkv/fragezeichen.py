"""
Downloaded mp3 files must be in a folder 'DDF' in the 'Downloads' directory
- Joins different chapters into a single mp3 file
- Adds id3 info and album art to the file
- Down-samples the file if it has a bit rate higher than 128k
"""

import os
import sys
import subprocess as sp
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TRCK, TALB, TPE1, TPE2, TDRC, APIC, ID3NoHeaderError

BIT_RATE = 128

PATH = os.environ['USERPROFILE'] + '\\Downloads\\DDF\\'  # mp3 files go here
FFMPEG = os.environ['USERPROFILE'] + '\\Miniconda3\\envs\\PyCharm\\Scripts\\ffmpeg.exe'  # location of ffmpeg.exe
COVERS = 'G:\\My Drive\\Coding\\render\\fragezeichen\\main\\static\\main\\cover\\'


class DDF:

    @staticmethod
    def check_ffmpeg():
        if not os.path.isfile(FFMPEG):
            sys.exit('ffmpeg.exe could not be found.')

    @staticmethod
    def extract_id3():
        try:
            for file in list(os.listdir(PATH))[::-1]:
                if file.endswith('.mp3'):  # Find the last mp3 file
                    print('\033[94m' + 'Extracting ID3 tags')
                    try:
                        tags = ID3(PATH + file)
                        album = str(tags['TALB'])
                    except ID3NoHeaderError:
                        tags = None
                        number, trunk = '', ''
                    else:
                        number = ''.join(c for c in album if c in '0123456789')
                        trunk = album.replace('Fragezeichen', '???')
                        trunk = trunk.split(' - ')[-1].split(': ')[-1].split('/')[-1].split('??? ')[-1]
                        trunk = ''.join([c for c in trunk if not c.isdigit()]).lstrip()

                    while not number.isdigit() or int(number) < 1 or int(number) > 999:
                        number = input('\033[94m' + 'Enter episode number: ')
                        if number.isdigit() and 0 < int(number) < 1000:
                            trunk = input('\033[94m' + 'Enter title: ')

                    if tags and 'TDRC' in tags:
                        year = str(tags['TDRC'])
                    else:
                        year = ''

                    while not year.isdigit() or int(year) < 1979 or int(year) > 2050:
                        year = input('\033[94m' + 'Enter release year: ')

                    conjunction = ''

                    if trunk == '':
                        trunk = input('\033[94m' + 'Enter title: ')

                    if trunk[0].isupper():
                        conjunction = '- '

                    number = int(number)
                    title = '%03d' % number + ' - ' + 'Die drei ??? ' + conjunction + trunk

                    return number, title, year
            sys.exit("No mp3 files found in 'DDF' folder")
        except FileNotFoundError:
            sys.exit("No folder 'DDF' in the 'Downloads' directory")

    @staticmethod
    def rename_forbidden_characters():
        files = [file for file in os.listdir(PATH) if file.endswith('.mp3')]
        for file in files:
            if "'" in file:
                DDF.rename(PATH + file, PATH + file.replace("'", ''))
            if 'ä' in file or 'ö' in file or 'ü' in file:
                DDF.rename(PATH + file, PATH + file.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue'))

    @staticmethod
    def join_chapters(number):
        print('\033[94m' + 'Joining chapters')
        files = [file for file in os.listdir(PATH) if file.endswith('.mp3')]
        txt = open('files.txt', 'w')
        for file in files:
            print('\033[93m' + file + ' \033[94m' + 'was found')
            txt.write("file '" + PATH + file + "'\n")
        txt.close()
        concat = os.environ['USERPROFILE'] + '\\Downloads\\' + 'concat.mp3'
        output = os.environ['USERPROFILE'] + '\\Downloads\\' + '%03d' % number + '.mp3'
        command1 = [FFMPEG, '-safe', '0', '-f', 'concat', '-i', 'files.txt', '-c', 'copy', concat]
        command2 = [FFMPEG, '-i', concat, '-acodec', 'copy', output]
        for command in [command1, command2]:
            pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 8)
            pipe.wait()
        os.remove('files.txt')
        os.remove(concat)
        return output

    @staticmethod
    def add_metadata(number, title, year, output):
        print('\033[94m' + 'Adding ID3 tags')
        tags = ID3(output)
        tags['TIT2'] = TIT2(encoding=3, text=title)        # title
        tags['TRCK'] = TRCK(encoding=3, text=str(number))  # number
        tags['TALB'] = TALB(encoding=3, text=title)        # album
        tags['TPE1'] = TPE1(encoding=3, text='???')        # contributing artist
        tags['TPE2'] = TPE2(encoding=3, text='???')        # album artist
        tags['TDRC'] = TDRC(encoding=3, text=year)         # year

        print('\033[94m' + 'Adding album art')
        print(COVERS + '%03d' % number + '.jpg')
        try:
            with open(COVERS + '%03d' % number + '.jpg', 'rb') as album_art:
                tags['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=album_art.read())
        except FileNotFoundError:
            print('\033[91m' + 'No album art found!')

        tags.save(output)

    @staticmethod
    def rename(old, new):
        if os.path.exists(new):
            os.remove(new)
        os.rename(old, new)

    @staticmethod
    def down_sample(file):
        bit_rate = MP3(file).info.bitrate / 1000
        print('\033[94m' + 'A bit rate of ' + '\033[93m' + str(bit_rate) + 'k ' + '\033[94m' + 'was found')
        if bit_rate > BIT_RATE:
            print('\033[94m' + 'Reducing bit rate')
            output = file.replace('.mp3', '_reduced.mp3')
            command = [FFMPEG, '-i', file, '-codec:a', 'libmp3lame', '-b:a', str(BIT_RATE) + 'k', output]
            pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 8)
            pipe.wait()
            DDF.rename(output, file)


def main():
    DDF.check_ffmpeg()
    number, title, year = DDF.extract_id3()
    DDF.rename_forbidden_characters()
    output = DDF.join_chapters(number)
    DDF.add_metadata(number, title, year, output)
    DDF.down_sample(output)
    print('\033[36m' + 'Complete!')


if __name__ == '__main__':
    main()
