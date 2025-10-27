'''
Sift through the data in the 'googlect_transit' folder containing static info about bus routes, times, etc
    and organize into per-route information
'''

import pandas as pd

folder_prefix = "googlect_transit"

# Grab pertinent info from routes.txt, trips.txt, stops.txt and stop_times.txt:
df_tripID_to_tripName = pd.read_csv(f"{folder_prefix}/trips.txt", dtype={"trip_id": "Int64", "trip_headsign": "str", "route_id": "Int64"})[["trip_id", "trip_headsign"]]

df_stopID_to_stopName = pd.read_csv(f"{folder_prefix}/stops.txt", dtype={"stop_id": "Int64", "stop_name": "str"})[["stop_id", "stop_name"]]

df_stopTimes_genInfo = pd.read_csv(f"{folder_prefix}/stop_times.txt", dtype={"trip_id": "Int64", "stop_sequence": "Int64", "stop_id": "Int64", "arrival_time": "str", "departure_time": "str"})[["trip_id", "stop_sequence", "stop_id", "arrival_time", "departure_time"]]

###
# Merge dataframes
###

df_stopsInfo = pd.merge(df_stopID_to_stopName, df_stopTimes_genInfo, how="right", on="stop_id")
df_allInfo = pd.merge(df_tripID_to_tripName, df_stopsInfo, how="right", on="trip_id")


###
# Temporary fix for rows with odd timestamps (values of '24' or '25' for the hour)
###
# Replace: 24 == 12am, 25 == 1am
df_allInfo = df_allInfo.replace({"arrival_time": r'^24:', "departure_time": r'^24:'}, {"arrival_time": '00:', "departure_time": '00:'}, regex=True)
df_allInfo = df_allInfo.replace({"arrival_time": r'^25:', "departure_time": r'^25:'}, {"arrival_time": '01:', "departure_time": '01:'}, regex=True)

output_file_path = "staticRouteInfo.csv"
df_allInfo.to_csv(f"{output_file_path}", index=False)
print(f"Completed, saved to {output_file_path}.")
