import requests
import json
import googlemaps
import re
from person import person


#when a new person is added to the database, we want to see who they are able to trade with
#a person can only trade with others in a 5 mile radius of themselves,
#we run through all the avaliable user locations and check who is within the 5 mile radius

class person_adder:
  
    #initialize the person_adder
    def __init__(self):
        
        #apikey here!
        self.mapClient = googlemaps.Client(key=apiKey)
        self.distanceThreshold = 5 #(distance in miles)

    #function obtains user address and calculate the coordinates
    def getCoordinates(self, currAddress):

        geoCodeResults = self.mapClient.geocode(currAddress)
        lat = geoCodeResults[0]["geometry"]["location"]["lat"]
        long = geoCodeResults[0]["geometry"]["location"]["lng"]
        return lat, long

    #function checks if two people can trade under the 5 mile rule
    def checkDistances(self, currAddress, otherAddress):

        #obtain distance between the two addresses (in miles)
        dist = self.mapClient.distance_matrix(currAddress, otherAddress)['rows'][0]['elements'][0]
        dist = dist["distance"]["text"]

        if ("km" in dist):
            dist = dist.replace(" km", "")
            dist = float(dist)
            dist = dist * 0.621371

        else: #distance is in meters (therefore nearby)
            dist = 0

        if (dist < self.distanceThreshold):
            print("can trade with: " + str(otherAddress))
            return True
        else:
            print("cannot trade with: " + str(otherAddress))
            return False

    #function to obtain possible meetup locations
    def getMeetupLocations(self, person):

        places = self.mapClient.places(location=(person.lat,person.lng), radius = 8046.72, type="library")
        for i in range(0, len(places)):
            print(places["results"][i]["formatted_address"])