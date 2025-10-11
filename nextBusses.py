# NextBusses

import requests
from time import localtime
import tkinter as tk
import tkinter.ttk as ttk

import json


######
#   Function definitions
######

def updateClock(lbl):
    curr_time = localtime()

    AM_or_PM = lambda t: "AM" if t < 12 else "PM"

    lbl.config(text=f"{curr_time.tm_hour if curr_time.tm_hour is not 0 else 12}:{curr_time.tm_min if curr_time.tm_min > 9 else "0"+str(curr_time.tm_min)}:{curr_time.tm_sec if curr_time.tm_sec > 9 else "0"+str(curr_time.tm_sec)} {AM_or_PM(curr_time.tm_hour)}")
    main.after(1000, updateClock, lbl)
###

def alertServerError(errCode):
    print(f"Error! Code: {errCode}")
###

def updateRouteInfo(routes, old_frame=None):
    if old_frame:
        old_frame.destroy()

    # Create new frame for the new info:
    info_frame = ttk.Frame(main, height=main.winfo_height(), width=main.winfo_width())
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

        data = response.json()["routes"][0]
        
        # Only look at public transit departure/arrival times:
        time_depart = ""
        time_arrival = ""

        steps = data["legs"][0]["steps"]
        for step in steps:
            print("checking step")
            if step["travelMode"] == "TRANSIT":
                time_depart = step["transitDetails"]["localizedValues"]["departureTime"]["time"]["text"]
                time_arrival = step["transitDetails"]["localizedValues"]["arrivalTime"]["time"]["text"]
                break
        ###

        ########

        ######
        #   Organize+output bus arrival info:
        ######        

        print(f"Route #{route_num} ({title} ) - Next at {time_depart}")

        bus_times_frame = ttk.Frame(info_frame, style="Bus.TFrame")

        route_label = ttk.Label(bus_times_frame, text=f"Route {route_num}", style="Bus.TLabel")
        route_label.grid(row=0, column=0)

        # Place space between sets of data:
        ttk.Label(bus_times_frame, text=" ", style="Bus.TLabel").grid(row=0, column=1, padx=150)

        route_time = ttk.Label(bus_times_frame, text=f"{time_depart}", style="Bus.TLabel")
        route_time.grid(row=0, column=4)

        route_desc = ttk.Label(bus_times_frame, text=f"{title}", style="Small.Bus.TLabel")
        route_desc.grid(row=1, column=0)

        bus_times_frame.grid(row=row_num, pady=20)  # Add new frame w/route info

        row_num += 1
    # End loop

    ######
    #   Update last-refresh time
    ######
    curr_time = localtime()
    AM_or_PM = lambda t: "AM" if t < 12 else "PM"
    ttk.Label(info_frame, text=f"Updates every 1 min.", style="Small.nonBus.TLabel").grid(row=row_num)
    ttk.Label(info_frame, text=f"Last updated: {curr_time.tm_hour if curr_time.tm_hour is not 0 else 12}:{curr_time.tm_min if curr_time.tm_min > 9 else "0"+str(curr_time.tm_min)} {AM_or_PM(curr_time.tm_hour)}",  style="nonBus.TLabel").grid(row=row_num+1)

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

main = tk.Tk()
main.title("Next Bus")
main.minsize(900, 700)
main.resizable(False, True)
main_bg_color = "#9BC1CF"
main.configure(bg=main_bg_color)

# Configure styles for later use:
style = ttk.Style()

busInfo_bg = "#012A36"

style.configure(".", background=main_bg_color, justify="center")
style.configure("TLabel", font="Helvetica, 16")
style.configure("Bus.TFrame", background=busInfo_bg)
style.configure("Bus.TLabel", font="Helvetica, 24", foreground="#fff", background=busInfo_bg, padding=4)
style.configure("Small.Bus.TLabel", font="Helvetica, 16")

style.configure("nonBus.TLabel", font="Helvetica 16")
style.configure("Small.nonBus.TLabel", font="Helvetica 12")


clock = ttk.Label(main, text="")
clock.pack(pady=20)
updateClock(clock)

updateRouteInfo(routes)

main.mainloop()  # Activate GUI

