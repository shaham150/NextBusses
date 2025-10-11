# NextBusses

# from urllib.request import urlopen
import requests
import json

def alertServerError(errCode):
    print(f"Error! Code: {errCode}")


# Import data for stored routes:
routes = []
time_arrival = ""  # Stored for later access

with open("routes.csv") as f:
    f.readline()  # Skip first line
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
        "X-Goog-FieldMask": "routes.legs"
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
        "travelMode": "TRANSIT"
    }

    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code != 200:
        alertServerError(response.status_code)
        break

    # print("Status code:", response.status_code)
    # print("Response text:", response.text)

    data = response.json()["routes"][0]["legs"]
    
    time_depart = data[0]["steps"][0]["transitDetails"]["localizedValues"]["departureTime"]["time"]["text"]
    time_arrival = data[0]["steps"][0]["transitDetails"]["localizedValues"]["arrivalTime"]["time"]["text"]

    print(f"Route #{route_num} ({title} ) - Next at {time_depart}")
###