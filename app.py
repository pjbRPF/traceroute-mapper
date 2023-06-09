from flask import Flask, render_template, request
import folium
import subprocess
import os
from geopy.geocoders import Nominatim

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/traceroute", methods=["POST"])
def traceroute():
    url = request.form.get("url")
    hop_list = run_traceroute(url)
    map_route = plot_route(hop_list)
    map_route.save("route_map.html")
    return "Success"

def run_traceroute(url):
    traceroute_output = subprocess.check_output(["traceroute", url]).decode("utf-8")
    hop_list = parse_traceroute_output(traceroute_output)
    print(hop_list)
    return hop_list

def parse_traceroute_output(output):
    hop_list = []
    lines = output.splitlines()
    for line in lines:
        if line.startswith(" "):
            hop_info = line.split()
            hop_ip = hop_info[1]
            hop_list.append(hop_ip)
    return hop_list

def plot_route(hop_list):
    # Create a map centered on the first hop
    geolocator = Nominatim(user_agent="traceroute_map")
    first_hop_location = geolocator.geocode(hop_list[0])
    map_route = folium.Map(location=[first_hop_location.latitude, first_hop_location.longitude], zoom_start=5)

    # Add markers for each hop
    for hop_ip in hop_list:
        location = geolocator.geocode(hop_ip)
        if location is not None:
            folium.Marker(
                location=[location.latitude, location.longitude],
                popup=hop_ip,
                icon=folium.Icon(icon="cloud")
            ).add_to(map_route)

    # Add lines connecting the markers
    for i in range(len(hop_list) - 1):
        start_location = geolocator.geocode(hop_list[i])
        end_location = geolocator.geocode(hop_list[i + 1])
        if start_location is not None and end_location is not None:
            folium.PolyLine(
                locations=[
                    [start_location.latitude, start_location.longitude],
                    [end_location.latitude, end_location.longitude]
                ],
                color='blue',
                weight=2,
                opacity=0.8
            ).add_to(map_route)

    map_route.save("route_map.html")
    return map_route

if __name__ == "__main__":
    app.run()