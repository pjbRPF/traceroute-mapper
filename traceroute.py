from flask import Flask, request
from flask_cors import CORS
import folium
from geopy.geocoders import Nominatim
from scapy.all import *

app = Flask(__name__)
CORS(app)

@app.route("/traceroute", methods=["POST"])
def run_traceroute():
    url = request.form.get("url")
    dest_latitude, dest_longitude, hop_list = traceroute(url)
    map_route = plot_route(dest_latitude, dest_longitude, hop_list)
    map_route.save("route_map.html")
    with open("route_map.html", "r") as f:
        return f.read()

def traceroute(url):
    # Remaining code stays the same

def plot_route(dest_latitude, dest_longitude, hop_list):
    # Remaining code stays the same

if __name__ == "__main__":
    app.run()
