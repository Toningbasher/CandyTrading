#main program: allows us to add users and view the exchange
from person import person
import pymongo
from person import person
from locationMatching import person_adder
import certifi #must include this so that the connection can be properly made
import googlemaps


def getMeetupLocations(person):
        #api key here
        mapClient = googlemaps.Client(key=apiKey)
        places = mapClient.places(location=(person.lat,person.lng), radius = 8046.72, type="library")
        for i in range(0, len(places)):
            print(places["results"][i]["formatted_address"])

def viewLocalCandies(collection):

    #find rows with Tradeable parameter
    query = {"Tradeable": {"$exists": True}}
    rows = collection.find(query)  

    for row in rows:

        print("current user has name: " + row.get("name"))
        otherUsers = row.get("Tradeable") #otherUsers should be an array

        #iterate through the potential trading partners
        for user in otherUsers:

            #perform the search query
            tempQuery = collection.find_one({"_id": user})
            print("local user willing to trade: " + tempQuery.get("name"))
            print("     candy: " + tempQuery.get("candy"))
            print("     quantity: " + tempQuery.get("quantity"))
            print("\n\n")

        #provide the potential trading locations
        print("trades can be conducted at the following libraries: ")
        tempPerson = person(row.get("name"), row.get("address"))
        tempPerson.lat = row.get("lat")
        tempPerson.lng = row.get("lng")
        getMeetupLocations(tempPerson)
        print("\n")



ca = certifi.where()
#cluster here
client = pymongo.MongoClient(cluster1, tlsCAFile=ca)
db = client["appData"]
collection = db["users"]

viewLocalCandies(collection)