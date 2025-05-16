# game.py

class Info:
    """
    A 2-dimensional array to store the map information.
    """

    FIELD = 'Field'
    INTERSECTION = 'Intersection'
    CROSSROAD = 'Crossroad'
    ROAD = 'Road'

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[None for _ in range(height)] for _ in range(width)]

    def get(self, x, y):
        return self.data[x][y]

    def setField(self, x, y):
        self.data[x][y] = self.FIELD

    def setIntersection(self, x, y, number):
        self.data[x][y] = (self.INTERSECTION, number)

    def setCrossroad(self, x, y, number):
        self.data[x][y] = (self.CROSSROAD, number)

    def setRoad(self, x, y, number):
        self.data[x][y] = (self.ROAD, number)


class Intersection:
    """
    An intersection in the map.
    """

    def __init__(self, number, positions):
        self.number = number
        self.positions = positions
        self.inRoads = []
        self.outRoads = []

    def getPositions(self):
        return self.positions

    def addInRoad(self, number):
        self.inRoads.append(number)

    def addOutRoad(self, number):
        self.outRoads.append(number)

    def getInRoads(self):
        return self.inRoads

    def getOutRoads(self):
        return self.outRoads


class Crossroad:
    """
    A crossroad in the map.
    """

    def __init__(self, number, positions):
        self.number = number
        self.positions = positions
        self.inRoads = []
        self.outRoads = []

    def getPositions(self):
        return self.positions

    def addInRoad(self, number):
        self.inRoads.append(number)

    def addOutRoad(self, number):
        self.outRoads.append(number)

    def getInRoads(self):
        return self.inRoads

    def getOutRoads(self):
        return self.outRoads


class Road:
    """
    A road in the map.
    """

    def __init__(self, number, positions, ways, start, end):
        self.number = number
        self.positions = positions
        self.ways = ways
        self.start = start
        self.end = end
        self.distance = len(positions)

    def getPositions(self):
        return self.positions

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getDistance(self):
        return self.distance

    def getIndexOfRoad(self, pos):
        return self.positions.index(pos)

    def getPosByIndex(self, index):
        if 0 <= index < self.distance:
            return self.positions[index]
        return None

    def getWayByIndex(self, index):
        if 0 <= index < self.distance:
            return self.ways[index]
        return None
