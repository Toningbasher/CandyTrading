#class stores the attributes of a person as we work with them
class person:

    #initialize the person
    def __init__(self, name, address):

        self.name = name
        self.address = address
        self.lat = 0
        self.lng = 0