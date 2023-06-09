import matplotlib.pyplot as plt
import geocoder
import subprocess

def get_coordinates(location):
    g = geocoder.arcgis(location)
    if g.ok:
        return g.latlng
    else:
        return None, None

def plot_traceroute(traceroute_results):
    x = []
    y = []
    locations = []

    for hop in traceroute_results:
        hop_data = hop.split()
        print(hop_data)
        if len(hop_data) >= 4:
            location = hop_data[3]
            latitude, longitude = get_coordinates(location)

            if latitude and longitude:
                x.append(latitude)
                y.append(longitude)
                locations.append(location)

    plt.figure(figsize=(10, 6))
    plt.plot(y, x, 'ro-', markersize=5)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Traceroute Map')

    for i, location in enumerate(locations):
        plt.annotate(location, (y[i], x[i]), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.show()

def run_traceroute(destination):
    try:
        process = subprocess.Popen(['traceroute', destination], stdout=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8')
        return output.split('\n')[1:-1]
    except Exception as e:
        print("Error running traceroute:", str(e))
        return []

if __name__ == '__main__':
    destination = input("Enter the destination address: ")
    traceroute_results = run_traceroute(destination)
    plot_traceroute(traceroute_results)
