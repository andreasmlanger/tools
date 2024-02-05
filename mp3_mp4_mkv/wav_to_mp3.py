"""
Converts wav files to mp3 files
The wav files need to be copied into the 'Downloads' directory
ffmpeg.exe needs to be in user directory
"""

import os
import subprocess as sp
import sys

PATH = os.path.join(os.environ['USERPROFILE'], 'Downloads')  # files go here
FFMPEG = os.path.join(os.environ['USERPROFILE'], 'Miniconda3', 'envs', 'PyCharm', 'Scripts', 'ffmpeg.exe')


class WAV:
    @staticmethod
    def convert_to_mp3():
        if not os.path.isfile(FFMPEG):
            sys.exit('ffmpeg.exe could not be found.')
        else:
            files = [f for f in os.listdir(PATH) if f.endswith('.wav')]
            if len(files) == 0:
                sys.exit("No wav files in 'Downloads' directory.")
            else:
                print('\033[94m' + 'The following wav files were found:')
                for file in files:
                    print('\033[93m' + file)
                print('\033[94m' + 'Press ENTER to start conversion')
                input()
                for file in files:
                    file_path = os.path.join(PATH, file)
                    output = os.path.join(PATH, f'{os.path.splitext(file)[0]}.mp3')
                    command = [FFMPEG, '-i', file_path, '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k', output]
                    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 8)
                    pipe.wait()
                print('\033[36m' + 'Conversion complete!' + '\033[99m')


def main():
    WAV.convert_to_mp3()


if __name__ == '__main__':
    main()
