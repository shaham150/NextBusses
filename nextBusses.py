# NextBusses

import requests
from time import localtime
from tkinter import *

import json


######
#   Function definitions
######

def updateClock(lbl):
    curr_time = localtime()

    AM_or_PM = lambda t: "AM" if t < 12 else "PM"

    lbl.config(text=f"Current Time:\n{curr_time.tm_hour if curr_time.tm_hour is not 0 else 12}:{curr_time.tm_min if curr_time.tm_min > 9 else "0"+str(curr_time.tm_min)}:{curr_time.tm_sec if curr_time.tm_sec > 9 else "0"+str(curr_time.tm_sec)} {AM_or_PM(curr_time.tm_hour)}")
    main.after(1000, updateClock, lbl)
###

def alertServerError(errCode):
    print(f"Error! Code: {errCode}")
###

def updateRouteInfo(routes, old_frame=None):
    if old_frame:
        old_frame.destroy()

    # Create new frame for the new info:
    info_frame = Frame(main, height=main.winfo_height(), width=main.winfo_width())
    info_frame.pack()

    row_num = 0  # Row number for grid organization

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

        data = response.json()["routes"][0]["legs"][0]["steps"]

        # print("JSON DUMP\n\n", json.dumps(data, indent=4))

        # Only look at public transit departure/arrival times:
        time_depart = ""
        time_arrival = ""
        for step in data:
            print("checking step")
            if step["travelMode"] == "TRANSIT":
                time_depart = step["transitDetails"]["localizedValues"]["departureTime"]["time"]["text"]
                time_arrival = step["transitDetails"]["localizedValues"]["arrivalTime"]["time"]["text"]
                break
        ###

        ########

        print(f"Route #{route_num} ({title} ) - Next at {time_depart}")

        route_info_label = Label(info_frame, text=f"Route {route_num} - {title} \n Next Departure: {time_depart}")
        route_info_label.grid(row=row_num)
        row_num += 1
    # End loop

    curr_time = localtime()
    AM_or_PM = lambda t: "AM" if t < 12 else "PM"
    Label(info_frame, text=f"Updates every 1 min.\nLast updated: {curr_time.tm_hour if curr_time.tm_hour is not 0 else 12}:{curr_time.tm_min if curr_time.tm_min > 9 else "0"+str(curr_time.tm_min)} {AM_or_PM(curr_time.tm_hour)}").grid(row=row_num)

    main.after(60000, lambda: updateRouteInfo(routes=routes, old_frame=info_frame))
###


######
#   One-time setup items
######

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


######
#   Create GUI
######

main = Tk()
main.title("Next Bus")
main.minsize(900, 700)

clock = Label(main, text="")
clock.pack()
updateClock(clock)

updateRouteInfo(routes)

main.mainloop()  # Activate GUI

