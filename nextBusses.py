# NextBusses

# from urllib.request import urlopen
import requests

# Import data for stored routes:
routes = []

with open("routes.csv") as f:
    for line in f:
        routes.append(line.split(";"))


api_key = ""
with open("api_key.txt") as f:
    api_key = f.read()


# Request data for each route:
for route in routes:
    print(route, len(route))
    route_num = route[0]
    title = route[1]
    origin_lat = float(route[2])
    origin_long = float(route[3])
    dest_lat = float(route[4])
    dest_long = float(route[5])

    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.distanceMeters,routes.duration,routes.polyline.encodedPolyline"
    }

    body = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": origin_lat,
                    "longitude": origin_long
                }
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": dest_lat,
                    "longitude": dest_long
                }
            }
        },
        "travelMode": "DRIVE"
    }

    response = requests.post(url, headers=headers, json=body)

    print("Status code:", response.status_code)
    print("Response text:", response.text)

    print(response.json())

