"""
Embeds a subtitle file into a video file
The files needs to be copied into the 'Downloads' directory
FFMPEG needs to be in user directory
"""

import os
import shutil
import subprocess as sp
import sys


PATH = os.path.join(os.environ['USERPROFILE'], 'Downloads')  # files go here
FFMPEG = os.path.join(os.environ['USERPROFILE'], 'Miniconda3', 'envs', 'PyCharm', 'Scripts', 'ffmpeg.exe')
HARD = True


class MP4:
    @staticmethod
    def embed_subtitle():
        if not os.path.isfile(FFMPEG):
            sys.exit('ffmpeg.exe could not be found.')
        else:
            files = [f for f in os.listdir(PATH) if f.endswith('.mp4') or f.endswith('.mkv')]
            subtitles = [f for f in os.listdir(PATH) if f.endswith('.vtt') or f.endswith('.srt')]
            if len(files) == 0 or len(subtitles) == 0:
                sys.exit("No mp4|mkv and vtt|srt files in 'Downloads' directory.")
            elif len(files) > 1 or len(subtitles) > 1:
                sys.exit("More than one mp4|mkv or vtt|srt file in 'Downloads' directory.")
            else:
                file = files[0]
                file_path = os.path.join(PATH, file)
                subtitle = subtitles[0]
                subtitle_path = os.path.join(PATH, subtitle)
                print('\033[94m' + 'The following file was found:\n' + '\033[93m' + file)
                print('\033[94m' + 'The following subtitle was found:\n' + '\033[93m' + subtitle)

                output = os.path.join(PATH, f'{os.path.splitext(file)[0]}_with_subtitle.mp4')
                target = f'temporary_subtitle{os.path.splitext(subtitle)[1]}'
                shutil.copyfile(os.path.join(PATH, subtitle), target)

                if HARD:
                    cmd = [FFMPEG, '-i', file_path, '-vf', 'subtitles=' + target, output]
                else:
                    cmd = [FFMPEG, '-i', file_path, '-i', subtitle_path, '-c', 'copy', '-c:s', 'mov_text', output]

                pipe = sp.Popen(cmd, stdout=sp.PIPE, bufsize=10 ** 8)
                pipe.wait()
                os.remove(target)
                print('\033[36m' + 'Embedding complete!')


def main():
    MP4.embed_subtitle()


if __name__ == '__main__':
    main()
