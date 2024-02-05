"""
Downloads a YouTube video as mp3 and webm file (optional subtitles)
ffmpeg.exe needs to be in user directory
"""

from yt_dlp import YoutubeDL
import os

SUBTITLES = False
MP3 = True
WEBM = False

PATH = os.path.join(os.environ['USERPROFILE'], 'Downloads')  # downloads go here
FFMPEG = os.path.join(os.environ['USERPROFILE'], 'Miniconda3', 'envs', 'PyCharm', 'Scripts', 'ffmpeg.exe')


class YouTube:
    @staticmethod
    def download():
        links = str(input('\033[94m' + 'Enter video links separated by space\n')).split(' ')
        for link in links:
            if link != '':
                v = {'outtmpl': PATH + r'\%(title)s.%(ext)s'}
                if SUBTITLES:
                    v['writeautomaticsub'] = True
                    v['allsubtitles'] = True
                if MP3:
                    a = {'outtmpl': PATH + r'\%(title)s.%(ext)s',
                         'format': 'bestaudio/best',
                         'postprocessors': [{'key': 'FFmpegExtractAudio',
                                             'preferredcodec': 'mp3',
                                             'preferredquality': '192'}]}
                    print('\033[92m' + 'Downloading audio file of ' + str(link))
                    with YoutubeDL(a) as ydl:
                        ydl.download([link])
                if WEBM:
                    print('\033[92m' + 'Downloading video file of ' + str(link))
                    with YoutubeDL(v) as ydl:
                        ydl.download([link])
                print('\033[36m' + 'All files downloaded successfully!')


def main():
    y = YouTube()
    y.download()


if __name__ == '__main__':
    main()
