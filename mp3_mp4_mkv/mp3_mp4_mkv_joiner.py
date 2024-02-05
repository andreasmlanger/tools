"""
Joins several mp3, mp4 or mkv files into a single file
The files need to be copied into a folder 'Files' in the 'Downloads' directory
FFMPEG folder needs to be in user directory
"""

import os
import subprocess as sp
import sys

FORMATS = ('.mp3', '.mp4', '.mkv')  # valid file formats

PATH = os.path.join(os.environ['USERPROFILE'], 'Downloads', 'Files')  # files go here
FFMPEG = os.path.join(os.environ['USERPROFILE'], 'Miniconda3', 'envs', 'PyCharm', 'Scripts', 'ffmpeg.exe')


class Mp3Mp4MKV:
    @staticmethod
    def join():
        if not os.path.isfile(FFMPEG):
            sys.exit('ffmpeg.exe could not be found.')
        else:
            try:
                files = [f for f in os.listdir(PATH) if f.endswith(FORMATS)]
            except FileNotFoundError:
                sys.exit("The files need to be copied into a folder 'Files' in the 'Downloads' directory")
            file_types = set()
            for file in files:
                print('\033[93m' + file + ' \033[94m' + 'was found')
                file_types.add(file.split('.')[-1])
            if len(file_types) > 1:
                sys.exit('Files of different file type cannot be joined.')
            elif len(files) < 2:
                sys.exit('There need to be at least two files for joining.')
            else:
                ending = file_types.pop()
                txt = open('files.txt', 'w')
                for file in files:
                    txt.write("file '" + os.path.join(PATH, file) + "'\n")
                txt.close()
                concat = os.path.join(os.path.dirname(PATH), f'concat.{ending}')
                output = os.path.join(os.path.dirname(PATH), f'joined_{ending}_files.{ending}')
                command1 = [FFMPEG, '-safe', '0', '-f', 'concat', '-i', 'files.txt', '-c', 'copy', concat]
                command2 = [FFMPEG, '-i', concat, '-acodec', 'copy', output]
                for command in [command1, command2]:
                    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 8)
                    pipe.wait()
                os.remove('files.txt')
                os.remove(concat)
                print('\033[36m' + 'Joining complete!')


def main():
    Mp3Mp4MKV.join()


if __name__ == '__main__':
    main()
