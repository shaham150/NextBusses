# NextBusses - Text-only testing version

import pandas as pd
from google.transit import gtfs_realtime_pb2 as gtfs  # From the MobilityData > awesome-transit repo on GitHub
from time import localtime

# Import dataframe from file:
try:
    df_route_info = pd.read_csv("staticRouteInfo.csv", low_memory=False)
except:
    raise Exception("File 'staticRouteInfo.csv' not found! Try generating a new one with 'ParseStaticRouteInfo.py'?")

# Convert time columns to datetime type:
df_route_info["arrival_time"] = pd.to_datetime(df_route_info["arrival_time"], format="%H:%M:%S").dt.time  # Convert series to timestamps
df_route_info["departure_time"] = pd.to_datetime(df_route_info["departure_time"], format="%H:%M:%S").dt.time  # Convert series to timestamps

# Store non-numeric route names for later checks:
non_numeric_route_names = [ name for name in df_route_info["route_short_name"].unique() if not name.isnumeric() ]


print("Please enter route number:")
selected_route = input("-> ")

# Repeatedly ask for input until valid, existing route number is recieved:
while ( selected_route not in non_numeric_route_names and not selected_route.isnumeric() ) or selected_route not in df_route_info["route_short_name"].unique():  
    print("\nInvalid route number.")
    print("\n\nPlease enter route number:")
    selected_route = input("-> ")

print(f"\nRoute number selected: {selected_route}")


###
# Sort dataframe by stop_sequence and pull out unique stop names for the chosen route:
print("\nPlease select a stop number from the list:")

df_currRoute_info = df_route_info.loc[ df_route_info["route_short_name"]==selected_route, : ]  # Find info only for selected route
stops_list = list(df_currRoute_info["stop_name"].unique())  # Create list of stop names on current route
stops_list.sort()  # Sort alphabetically

print("Reference Number:     Stop Name:")
for stop in range(1, len(stops_list)+1):
    print(f"               {stop}       { stops_list[stop-1] }")

print("Enter reference number of stop to select:")
selected_stop = input("-> ")

# Force valid input:
while not selected_stop.isnumeric() or int(selected_stop) < 1 or int(selected_stop) >= len(stops_list):
    print("Invalid input.")
    print("\nEnter reference number of stop to select:")
    selected_stop = input("-> ")

selected_stop = stops_list[int(selected_stop)-1]  # Store name of selected stop

print(f"SELECTED: {selected_route}, {selected_stop}")


curr_timestamp = pd.to_datetime(f"{localtime().tm_hour}:{localtime().tm_min}:{localtime().tm_sec}", format="%H:%M:%S").time()  # Create timestamp of current time
next_time = df_route_info.loc[ (df_route_info["route_short_name"] == selected_route) & (df_route_info["stop_name"] == selected_stop) & (df_route_info["arrival_time"] >= curr_timestamp) ].sort_values(by="arrival_time")["arrival_time"].iloc[0]  # Find the next-closest arrival time (current-time inclusive)

print(f"The next bus will arrive at: {next_time}")