"""
Cuts mp3, mp4 or mkv file
The file needs to be copied into the 'Downloads' directory
FFMPEG folder needs to be in user directory
"""

import eyed3
from mutagen.id3 import ID3, APIC
from PIL import Image
from io import BytesIO
import os
import subprocess as sp
import sys

FORMATS = ('.mp3', '.mp4', '.mkv')  # valid file formats

PATH = os.path.join(os.environ['USERPROFILE'], 'Downloads')  # file goes here
FFMPEG = os.path.join(os.environ['USERPROFILE'], 'Miniconda3', 'envs', 'PyCharm', 'Scripts', 'ffmpeg.exe')


class Mp3Mp4MKV:
    @staticmethod
    def get_time_input(value):
        print('\033[94m' + f'Enter {value} time in seconds or press ENTER to skip')
        x = input()
        while not (x.replace('.', '', 1).replace(':', '', 2).isnumeric() or x == ''):
            print('\033[91m' + 'No valid time.')
            x = input()
        if ':' in x:
            x = str(sum(float(y) * 60 ** i for i, y in enumerate(reversed(x.split(':')))))  # e.g. 0:01:15
        if value == 'start' and x == '':
            x = '0'
        return x

    @staticmethod
    def get_format_input(file):
        print('\033[94m' + 'Enter desired format (e.g. mp3, mp4, mkv) or press ENTER to skip')
        name, extension = os.path.splitext(file)
        x = input()
        if f'.{x}' in FORMATS:
            return os.path.join(PATH, f'{name}_cut.{x}')
        return os.path.join(PATH, f'{file}_cut{extension}')

    @staticmethod
    def get_speed_input(file, output):
        if not file.endswith('mp3') and output.endswith('mp3'):
            return '1.0'
        print('\033[94m' + 'Enter desired speed (e.g. 1.25) or press ENTER to skip')
        try:
            return str(float(input()))
        except ValueError:
            return '1.0'

    @staticmethod
    def update_album_art_in_mp3(file, output):
        file_path = os.path.join(PATH, file)
        cover_path = os.path.join(PATH, 'cover.jpg')
        audiofile = eyed3.load(file_path)
        if audiofile.tag.frame_set.get(b'APIC'):
            album_art_data = audiofile.tag.frame_set[b'APIC'][0].image_data
            im = Image.open(BytesIO(album_art_data))
            im.show()  # show album art
            im.save(cover_path, 'JPEG', quality=100, optimize=True, progressive=True)
            tags = ID3(output)
            with open(cover_path, 'rb') as album_art:
                tags['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=album_art.read())
            tags.save(output)
            os.remove(cover_path)
            print('\033[94m' + 'Album art updated!')
        else:
            print('\033[94m' + 'No album art found in mp3 file!')

    @staticmethod
    def cut():
        if not os.path.isfile(FFMPEG):
            sys.exit('ffmpeg.exe could not be found.')
        else:
            files = [file for file in os.listdir(PATH) if file.endswith(FORMATS)]
            if len(files) == 0:
                sys.exit("No mp3|mp4|mkv files in 'Downloads' directory.")
            elif len(files) > 1:
                sys.exit("More than one mp3|mp4|mkv file in 'Downloads' directory.")
            else:
                file = files[0]
                file_path = os.path.join(PATH, file)
                print('\033[94m' + 'The following file was found:\n' + '\033[93m' + file)

                start = Mp3Mp4MKV.get_time_input('start')
                end = Mp3Mp4MKV.get_time_input('end')
                output = Mp3Mp4MKV.get_format_input(file)
                speed = Mp3Mp4MKV.get_speed_input(file, output)

                if not file.endswith('mp3') and output.endswith('mp3'):
                    codecs = ['-c:a', 'libmp3lame']
                elif speed != '1.0':
                    s = '[0:v]setpts=' + str(1 / float(speed)) + '*PTS[v];[0:a]atempo=' + speed + '[a]'
                    codecs = ['-filter_complex', s, '-map', '[v]', '-map', '[a]']
                else:
                    codecs = ['-c:a', 'copy']

                if end:
                    command = [FFMPEG, '-i', file_path] + codecs + ['-ss', start, '-to', end, output]
                else:
                    command = [FFMPEG, '-i', file_path] + codecs + ['-ss', start, output]

                pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 8)  # cut
                pipe.wait()

                if file.endswith('.mp3'):
                    Mp3Mp4MKV.update_album_art_in_mp3(file, output)

                print('\033[36m' + 'Cutting complete!')


def main():
    Mp3Mp4MKV.cut()


if __name__ == '__main__':
    main()
