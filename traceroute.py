import folium
from geopy.geocoders import Nominatim
from scapy.all import *

def traceroute(url):
    # Remaining code stays the same

# Prompt the user for a URL
url = input("Enter a URL to trace: ")

# Perform traceroute
dest_latitude, dest_longitude, hop_list = traceroute(url)

# Plot the route on a map
map_route = plot_route(dest_latitude, dest_longitude, hop_list)
map_route.save("route_map.html")