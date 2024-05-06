"""
Several useful functions for working with gpx files and folium maps
"""

import gpxpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import concurrent.futures
import math
import os
import time
from xml.etree import ElementTree


N = 99  # parameter for elevation smoothing (rolling average)


def gpx_to_df(file_name, directory=''):
    """
    Loads a gpx file with a single track and returns a df
    """
    file_path = os.path.join(directory, file_name)
    with open(file_path) as f:
        gpx = gpxpy.parse(f)
        track = gpx.tracks[0]
        segment = track.segments[0]
        data = [(round(p.latitude, 5), round(p.longitude, 5), p.elevation) for p in segment.points]
        df = pd.DataFrame(data, columns=['lat', 'lon', 'elevation'])
        return df


def df_to_gpx(df, directory='', file_name='NEW'):
    """
    Converts df back to gpx file
    """
    gpx_root = ElementTree.Element('gpx', version='1.1', xmlns='http://www.topografix.com/GPX/1/1')
    track = ElementTree.SubElement(gpx_root, 'trk')
    track_name = ElementTree.SubElement(track, 'name')
    track_name.text = file_name
    track_segment = ElementTree.SubElement(track, 'trkseg')

    latitudes = df['lat'].astype(str)
    longitudes = df['lon'].astype(str)
    if 'elevation' in df.columns:
        elevations = df['elevation'].astype(int).astype(str)
        for lat, lon, ele in zip(latitudes, longitudes, elevations):
            track_point = ElementTree.SubElement(track_segment, 'trkpt', lat=lat, lon=lon)
            elevation = ElementTree.SubElement(track_point, 'ele')
            elevation.text = str(int(ele))
    else:
        for lat, lon in zip(latitudes, longitudes):
            ElementTree.SubElement(track_segment, 'trkpt', lat=lat, lon=lon)

    tree = ElementTree.ElementTree(gpx_root)
    ElementTree.indent(tree, '  ')
    file_path = os.path.join(directory, f'{file_name}.gpx')
    tree.write(file_path, encoding='utf-8', xml_declaration=True)


def add_elevation_to_df(df, file='', show_profile=False, smoothing=False):
    elevation_dict = {'Error': ''}  # only contains 'Error' placeholder

    while True:
        batches = get_lat_lon_without_elevation(df)
        print(f' Adding elevations ({len(batches)}): ', end='')
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:  # thread pool defining max of threads
            futures = [executor.submit(add_elevation, lat, lon, elevation_dict) for lat, lon in batches]
            concurrent.futures.wait(futures)
            print(' OK')
        df['elevation'] = df.apply(lambda r: get_elevation(r, elevation_dict), axis=1)
        if elevation_dict['Error']:
            print(f' {elevation_dict["Error"]}\n ', end='')
            elevation_dict['Error'] = ''  # clear error
            time.sleep(300)  # pause for 5 minutes
        else:
            break

    df = smooth_elevation_profile(df, file, show_profile, smoothing)
    return df


def get_lat_lon_without_elevation(df):
    df = df[df['elevation'].isna()]
    batches = [(lat, lon) for lat, lon in zip(df['lat'], df['lon'])]
    batches = list(set(batches))  # remove duplicates
    return batches


def get_elevation(r, elevation_dict):
    if r['elevation'] is not None:
        return r['elevation']
    elif (r['lat'], r['lon']) in elevation_dict:
        return elevation_dict[(r['lat'], r['lon'])]


def add_elevation(lat, lon, elevation_dict):
    """
    Adds integer elevation to mutable elevation_dictionary, using (latitude, longitude) as key
    """
    if elevation_dict['Error']:
        return  # return gracefully if error

    key, elevation = fetch_elevation(lat, lon)
    elevation_dict[key] = elevation

    if len(elevation_dict) % 100 == 0:
        print('#', end='')  # print progress


def fetch_elevation(lat, lon):
    """
    Fetches elevation via Open-Meteo API GET request
    """
    url = 'https://api.open-meteo.com/v1/elevation'
    while True:
        try:
            response = requests.get(f'{url}?latitude={lat}&longitude={lon}')
            json = response.json()
            if 'elevation' in json:
                return (lat, lon), json['elevation'][0]
            else:
                return 'Error', json['reason']
        except Exception as ex:
            print(ex)


def smooth_elevation_profile(df, file, show_profile, smoothing):
    if show_profile:
        df = add_distance_to_df(df)
        plt.plot(df['distance'], df['elevation'], color='black', alpha=0.2)
    if smoothing:
        df['elevation'] = df['elevation'].rolling(N, center=True, min_periods=1).mean()
    if show_profile:
        plt.plot(df['distance'], df['elevation'])
        plt.xlabel('Distance (km)')
        plt.ylabel('Elevation (m)')
        plt.title(file)
        plt.show()
    return df


def add_distance_to_df(df):
    """
    Adds a 'distance' column to a df with columns 'latitude' and 'longitude'
    """
    df[['lat_shift', 'lon_shift']] = df[['lat', 'lon']].shift(1)
    df['distance'] = df.apply(lambda r: distance(r['lat'], r['lon'], r['lat_shift'], r['lon_shift']), axis=1)
    df['distance'] = df['distance'].cumsum().fillna(0)
    df = df.drop(['lat_shift', 'lon_shift'], axis=1)
    return df


def distance(lat1, lon1, lat2, lon2):
    """
    Calculates distance in km between two coordinates
    """
    earth_radius = 6371  # Earth's radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = earth_radius * c
    return d


def calculate_elevation_gain_and_drop(df):
    """
    Returns elevation gain and drop in meters from a df with 'elevation' column (both as positive integer)
    """
    df = df.copy()
    df['elevation_shift'] = df['elevation'].shift(1)
    df['elevation_change'] = df['elevation'] - df['elevation_shift']
    df['gain'] = np.maximum(df['elevation_change'], 0)
    df['drop'] = np.minimum(df['elevation_change'], 0)
    return int(df['gain'].sum()), -int(df['drop'].sum())
