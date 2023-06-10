import socket
import json
import requests
import folium
from scapy.all import IP, ICMP, sr

def get_location(ip_address):
    access_token = "a10667d394060a"
    url = f"https://ipinfo.io/{ip_address}/json?token={access_token}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        if "loc" in data:
            lat, lng = data["loc"].split(",")
            return float(lat), float(lng)
    return None

def run_traceroute(destination):
    traceroute_results = []
    try:
        dest_ip = socket.gethostbyname(destination)
        for ttl in range(1, 31):
            packet = IP(dst=dest_ip, ttl=ttl) / ICMP()
            reply = sr(packet, verbose=False, timeout=5)
            if reply[0]:
                src_ip = reply[0][0][1].src
                traceroute_results.append({"hop": ttl, "ip": src_ip})
        print(traceroute_results) ## DEBUG
    except socket.gaierror:
        print(f"Unable to resolve the destination: {destination}")
    return traceroute_results

def plot_traceroute(traceroute_results):
    traceroute_map = folium.Map(location=[0, 0], zoom_start=2)
    for hop in traceroute_results:
        ip_address = hop['ip']
        location = get_location(ip_address)
        if location:
            folium.Marker(location, popup=ip_address).add_to(traceroute_map)
    traceroute_map.save("traceroute_map.html")
    print("Traceroute map generated. Please download 'traceroute_map.html' and open it in a web browser to view the map.")

# Example usage
destination = input("Enter a URL to trace: ")
traceroute_results = run_traceroute(destination)
plot_traceroute(traceroute_results)
