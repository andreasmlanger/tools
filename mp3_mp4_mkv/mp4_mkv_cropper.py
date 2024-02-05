"""
Crops a mkv or mp4 file (x-width, y-width, x-offset, y-offset from top-left)
The file needs to be copied into the 'Downloads' directory
FFMPEG and FFPROBE need to be in user directory
"""

import os
import subprocess as sp
import sys

PATH = os.path.join(os.environ['USERPROFILE'], 'Downloads')  # files go here
FFMPEG = os.path.join(os.environ['USERPROFILE'], 'Miniconda3', 'envs', 'PyCharm', 'Scripts', 'ffmpeg.exe')
FFPROBE = os.path.join(os.environ['USERPROFILE'], 'Miniconda3', 'envs', 'PyCharm', 'Scripts', 'ffprobe.exe')


class MP4:
    @staticmethod
    def crop():
        if not os.path.isfile(FFMPEG):
            sys.exit('ffmpeg.exe could not be found.')
        else:
            files = [f for f in os.listdir(PATH) if f.endswith('.mp4') or f.endswith('.mkv')]
            if len(files) == 0:
                sys.exit("No MP4|MKV files in 'Downloads' directory.")
            elif len(files) > 1:
                sys.exit("More than one MP4|MKV file in 'Downloads' directory.")
            else:
                file = files[0]
                file_path = os.path.join(PATH, file)
                print('\033[94m' + 'The following file was found:\n' + '\033[93m' + file, end=' | ')

                # Get dimensions
                command = [FFPROBE, '-v', 'error', '-of', 'flat=s=_', '-select_streams', 'v:0', '-show_entries',
                           'stream=height,width', file_path]

                pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 8)
                pipe.wait()
                w, h = map(int, [d.split('=')[-1] for d in pipe.communicate()[0].decode('utf-8').split('\n')[:2]])
                print(f'{w} x {h} px')

                print('\033[94m' + "Enter new dimensions, e.g. '960 560 300 110' or '1280 575 0 95'", end='')
                print(' (x-width y-width x-offset y-offset from top-left)')
                dimensions = input()
                while not (dimensions.replace(' ', '').isnumeric()):
                    print('\033[91m' + 'No valid dimensions.')
                    dimensions = input()

                dimensions = ':'.join(dimensions.split())

                name, extension = os.path.splitext(file)
                output = os.path.join(PATH, f'{name}_cropped{extension}')

                # Crop
                command = [FFMPEG, '-i', file_path, '-filter:v', 'crop=' + dimensions, '-c:a', 'copy', output]

                pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 8)
                pipe.wait()

                print('\033[36m' + 'Cropping complete!')


def main():
    MP4.crop()


if __name__ == '__main__':
    main()
