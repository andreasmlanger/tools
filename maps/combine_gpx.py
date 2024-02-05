"""
Combines multiple gpx files into a single gpx file
"""

import pandas as pd
import os
import sys
from utils import gpx_to_df, df_to_gpx


PATH = os.environ['USERPROFILE'] + '\\Downloads\\'  # files go here


class GPX:
    @staticmethod
    def join(files):
        df_list = [gpx_to_df(file, directory=PATH) for file in files]
        df = pd.concat(df_list)
        df = df.dropna(axis=1)
        df_to_gpx(df, directory=PATH, file_name='joined_gpx')
        print('\033[36m' + 'Joining complete!')


def main():
    files = [file for file in os.listdir(PATH) if file.endswith('.gpx')]
    if len(files) < 2:
        sys.exit("No gpx files in 'Downloads' directory")
    GPX().join(files)


if __name__ == '__main__':
    main()
