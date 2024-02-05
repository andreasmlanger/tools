"""
Converts csv files to gpx files
"""

import os
import sys
import pandas as pd
from utils import df_to_gpx


PATH = os.environ['USERPROFILE'] + '\\Downloads\\'  # files go here


class GPX:
    @staticmethod
    def csv_to_gpx(file):
        print(' Converting to gpx:', end='')
        file_path = os.path.join(PATH, file)
        df = pd.read_csv(file_path)
        df_to_gpx(df, directory=PATH, file_name=file[:-4])
        print(' OK')


def main():
    files = [file for file in os.listdir(PATH) if file.endswith('.csv')]
    if len(files) == 0:
        sys.exit("No csv files in 'Downloads' directory")
    for file in files:
        print('\033[38m' + 'Found ' + '\033[93m' + file + '\033[38m' + ':')
        GPX().csv_to_gpx(file)


if __name__ == '__main__':
    main()
