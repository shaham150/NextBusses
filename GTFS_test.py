import requests
from google.transit import gtfs_realtime_pb2 as gtfs  # From the MobilityData > awesome-transit repo on GitHub


feed = gtfs.FeedMessage()  # Create object
response = requests.get("https://cttprdtmgtfs.ctttrpcloud.com/TMGTFSRealTimeWebService/TripUpdate/TripUpdates.pb")
feed.ParseFromString(response.content)  # Stores to 'feed' obj (?)

for entity in feed.entity:
    print(entity)
    print("\n\n END ENTITY \n-----------\n NEW ENTITY START\n\n")

##