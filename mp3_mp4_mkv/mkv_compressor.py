"""
Compresses mkv|mp4 files to fit on a mobile device
The mkv|mp4 files need to be copied into the 'Downloads' directory
ffmpeg.exe needs to be in user directory
"""

import os
import subprocess as sp
import sys

FORMATS = ('.mp4', '.mkv', '.avi')  # valid file formats
EXTENSION = '.mkv'  # file type of compressed file

PATH = os.path.join(os.environ['USERPROFILE'], 'Downloads')  # files go here
FFMPEG = os.path.join(os.environ['USERPROFILE'], 'Miniconda3', 'envs', 'PyCharm', 'Scripts', 'ffmpeg.exe')


class Video:
    @staticmethod
    def compress():
        if not os.path.isfile(FFMPEG):
            sys.exit('ffmpeg.exe could not be found.')
        else:
            files = [f for f in os.listdir(PATH) if f.endswith(FORMATS)]
            if len(files) == 0:
                sys.exit("No MP4|MKV|AVI files in 'Downloads' directory.")
            else:
                print('\033[94m' + 'The following MP4|MKV|AVI files were found:')
                for file in files:
                    print('\033[93m' + file)
                print('\033[94m' + 'Press ENTER to start compression')
                input()
                for f in files:
                    file_name, extension = os.path.splitext(f)
                    output = os.path.join(PATH, f'{file_name}_compressed{EXTENSION}')
                    command = [FFMPEG, '-i', os.path.join(PATH, f), '-vcodec', 'h264', '-acodec', 'mp3', output]
                    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 8)
                    pipe.wait()
                print('\033[36m' + 'Compression complete!' + '\033[99m')


def main():
    Video.compress()


if __name__ == '__main__':
    main()
