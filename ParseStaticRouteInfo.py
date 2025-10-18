'''
Sift through the data in the 'googlect_transit' folder containing static info about bus routes, times, etc
    and organize into per-route information
'''

import pandas as pd

folder_prefix = "googlect_transit"

# Grab pertinent info from routes.txt, trips.txt, stops.txt and stop_times.txt:
df_routes_genInfo = pd.read_csv(f"{folder_prefix}/routes.txt")[["route_id", "route_short_name", "route_long_name"]]

df_tripID_to_routeID = pd.read_csv(f"{folder_prefix}/trips.txt")[["trip_id", "route_id"]]

df_stops_genInfo = pd.read_csv(f"{folder_prefix}/stops.txt")[["stop_id", "stop_name"]]

df_stopTimes_genInfo = pd.read_csv(f"{folder_prefix}/stop_times.txt")[["trip_id", "stop_sequence", "stop_id", "arrival_time", "departure_time"]]

###
# Merge dataframes
###

df_stopsInfo = pd.merge(df_stops_genInfo, df_stopTimes_genInfo, how="right", on="stop_id")
df_trip_to_stops = pd.merge(df_tripID_to_routeID, df_stopsInfo, how="right", on="trip_id")
df_allInfo = pd.merge(df_routes_genInfo, df_trip_to_stops, how="right", on="route_id")

output_file_path = "staticRouteInfo.csv"
df_allInfo.to_csv(f"{output_file_path}", index=False)
print(f"Completed, saved to {output_file_path}.")
