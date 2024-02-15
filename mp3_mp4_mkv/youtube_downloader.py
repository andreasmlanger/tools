"""
Downloads a YouTube video as mp4 and mp3 file
"""

from pytube import YouTube
import os

PATH = os.path.join(os.environ['USERPROFILE'], 'Downloads')  # downloads go here


class YT:
    @staticmethod
    def download(yt, output_format='mp4'):
        if output_format == 'mp4':
            yt.streams.filter(
                progressive=True,
                file_extension='mp4',
            ).order_by('resolution').desc().first().download(output_path=PATH)

        elif output_format == 'mp3':
            yt.streams.filter(
                only_audio=True,
            ).order_by('abr').desc().first().download(output_path=PATH)


def main():
    urls = str(input('Enter YouTube video urls separated by space: ')).split(' ')
    for url in urls:
        yt = YouTube(url)
        YT.download(yt, 'mp4')
        YT.download(yt, 'mp3')
    print('\033[36m' + 'All files downloaded successfully!')


if __name__ == '__main__':
    main()
