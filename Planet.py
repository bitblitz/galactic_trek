from ISectorContent import ISectorContent


class Planet(ISectorContent):
    def __init__(self, coord):
        self.type = 'M'
        self.coordinate = coord  # create a place to store the coordinate for the object, but don't initialize it yet

    def asChar(self):
        return '+'
