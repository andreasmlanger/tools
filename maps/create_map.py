"""
Creates a folium map html from a gpx file
"""

import folium
from folium.plugins import Fullscreen
import gpxpy
import os
import sys
import webbrowser


PATH = os.environ['USERPROFILE'] + '\\Downloads\\'  # files go here


class MAP:
    def create_map(self, files):
        # Create new Folium map
        f = folium.Figure()
        m = folium.Map(zoom_control=False).add_to(f)

        # Change tile layer to terrain
        tile_layer = folium.TileLayer('http://tile.stamen.com/terrain/{z}/{x}/{y}.jpg', attr='©Fuchs')
        tile_layer.add_to(m)

        all_points = []

        for file in files:
            with open(os.path.join(PATH, file)) as gpx_file:
                gpx = gpxpy.parse(gpx_file)

                # Extract points into list as tuples
                points = []
                for track in gpx.tracks:
                    for segment in track.segments:
                        for point in segment.points:
                            points.append((point.latitude, point.longitude))
                all_points.extend(points)

                # Add a polyline to the map using the GPS track points
                folium.PolyLine(points, color='blue').add_to(m)

                # Add start and end markers
                def create_icon(color):
                    return folium.Icon(color=color, icon_color='white', icon='bicycle', prefix='fa')

                def create_popup(text):
                    return folium.Popup(f'<h5>{text}</h5>', max_width=400)

                folium.Marker(points[0], popup=create_popup('START'), icon=create_icon('green')).add_to(m)
                folium.Marker(points[-1], popup=create_popup('END'), icon=create_icon('red')).add_to(m)

        # Find bounds and ideal zoom
        m.fit_bounds(self.get_bounds(all_points))

        # Add full-screen option
        Fullscreen().add_to(m)

        # Save the map
        m.save(os.path.join(PATH, 'map.html'))
        print('\033[36m' + 'Map created!')

        # Open the map
        webbrowser.open(os.path.join(PATH, 'map.html'))

    @staticmethod
    def get_bounds(points):
        min_lat = min([p[0] for p in points])
        max_lat = max([p[0] for p in points])
        min_lon = min([p[1] for p in points])
        max_lon = max([p[1] for p in points])
        border_lat = 0.1 * abs(min_lat - max_lat)
        border_lon = 0.1 * abs(min_lon - max_lon)
        return [(min_lat - border_lat, min_lon - border_lon), (max_lat + border_lat, max_lon + border_lon)]


def main():
    files = [file for file in os.listdir(PATH) if file.endswith('.gpx')]
    if len(files) == 0:
        sys.exit("No gpx files in 'Downloads' directory")
    MAP().create_map(files)


if __name__ == '__main__':
    main()
