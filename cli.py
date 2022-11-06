#main program: allows us to add users and view the exchange
from person import person
import pymongo
from person import person
from locationMatching import person_adder
import certifi #must include this so that the connection can be properly made

#helper functions:
def updateCollection(collection):

    for row in collection.find():
        
        #parse the address: (get value using the key)
        currAddress = row.get("address")
        currName = row.get("name")
        
        #get the person object and get the distances
        tempPerson = person(currName, currAddress)
        tempPerson.lat, tempPerson.lng = adder.getCoordinates(tempPerson.address)
        
        collection.find_one_and_update({"_id": row.get("_id")}, {"$set" :{"lat": tempPerson.lat}})
        collection.find_one_and_update({"_id": row.get("_id")}, {"$set" :{"lng": tempPerson.lng}})
        
        #double loop through the database and determine who can trade with the current person
        for row2 in collection.find():
            
            #if the 2nd row is different from the current
            if (row.get("_id") != row2.get("_id")):
                
                #compare the distance between the two people
                #if returns true then we can trade with the person
                if (adder.checkDistances(currAddress, row2.get("address"))):
                    
                    #add the person to the list to trade with
                    #check so no duplicates
                    collection.find_one_and_update({"_id": row.get("_id")}, {"$push": {"Tradeable": row2.get("_id")}})

def viewLocalCandies(collection):
    
    #read a single user in the database
    row = collection.find_one()
    otherUsers = row.get("Tradeable")
    print(otherUsers)

    for user in otherUsers:

        tempQuery = collection.find({"_id": user})
        candy = tempQuery.get("candy")
        quantity = tempQuery.get("quantity")



#database connection
ca = certifi.where()
#database cluster here
client = pymongo.MongoClient(cluster1, tlsCAFile=ca)
db = client["appData"]
collection = db["users"]

#adder object (helps add information to the database)
adder = person_adder()

while (True):
    
    print("Enter User name (or -1 to continue):")
    action = input()
    if (action != "-1"):
        name = action
    else:
        break
    print("Enter Address:")
    address = input()

    #contain information about candy
    print("Enter Candy Name:")
    candyName = input()
    print("Enter Candy Quantity:")
    candyQuantity = input()

    #add relevant information to the database
    tempPerson = person(name, address)
    initialData = {"name": name, "address": address, "candy": candyName, "quantity": candyQuantity}
    collection.insert_one(initialData)
    updateCollection(collection)