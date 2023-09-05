import folium
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/map', methods=['POST'])
def show_map():
    coordinates = request.form['coordinates']
    lat, lon = coordinates.split(
        ',')  # Assuming coordinates are in the format "latitude,longitude"

    # Create a Folium map centered on the coordinates
    map_obj = folium.Map(location=[float(lat), float(lon)], zoom_start=25)

    # Add a marker to the map
    folium.Marker([float(lat), float(lon)]).add_to(map_obj)

    # Save the map as an HTML file
    map_obj.save('templates/map.html')

    return render_template('map.html')


if __name__ == '__main__':
    app.run()
