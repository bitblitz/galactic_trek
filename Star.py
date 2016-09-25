from ISectorContent import ISectorContent


class Star(ISectorContent):
    def __init__(self, coord):
        self.coordinate = coord

    def asChar(self):
        return '*'
