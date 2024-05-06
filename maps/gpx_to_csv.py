"""
Converts gpx files to csv files, adding elevation using the open-meteo API
"""

import os
import sys
from utils import add_distance_to_df, add_elevation_to_df, calculate_elevation_gain_and_drop, df_to_gpx, gpx_to_df


PATH = os.environ['USERPROFILE'] + '\\Downloads\\'  # files go here
ADD_ELEVATION = True
SHOW_PROFILE = True  # display elevation profile after each addition of elevation data
SMOOTHING = True


class GPX:
    @staticmethod
    def add_elevation_to_gpx_file(file):
        df = gpx_to_df(file, directory=PATH)
        df = add_elevation_to_df(df, file=file, show_profile=SHOW_PROFILE, smoothing=SMOOTHING)
        df_to_gpx(df, directory=PATH, file_name=file[:-4])  # overwrite!

    @staticmethod
    def gpx_to_csv(file):
        print(' Converting to csv:', end='')
        df = gpx_to_df(file, directory=PATH)
        df = add_distance_to_df(df)
        df = df.drop_duplicates()
        km = int(df['distance'].iloc[-1])
        df.columns = ['lat', 'lon', 'elevation', 'distance']
        if df['elevation'].isnull().values.any():
            df = df[['lat', 'lon']]
            file_name = f'{file.split(".")[0]}_{km}km.csv'
        else:
            up, down = calculate_elevation_gain_and_drop(df)
            file_name = f'{file.split(".")[0]}_{km}km_{up}m_{down}m.csv'
        df.to_csv(os.path.join(PATH, file_name), index=False)
        print(' OK')


def main():
    files = [file for file in os.listdir(PATH) if file.endswith('.gpx')]
    if len(files) == 0:
        sys.exit("No gpx files in 'Downloads' directory")
    for file in files:
        print('\033[38m' + 'Found ' + '\033[93m' + file + '\033[38m' + ':')
        if ADD_ELEVATION:
            GPX().add_elevation_to_gpx_file(file)
        GPX().gpx_to_csv(file)


if __name__ == '__main__':
    main()
