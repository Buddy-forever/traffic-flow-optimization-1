# simulate.py

from time import sleep
from car import CarMap

class Car(object):
    """
    A car in simulation.
    """

    def __init__(self, idd, dirs):
        self.stepLeft = dirs[0]
        self.dirs = dirs[1]
        self.timeStamp = 0

    def isArrived(self):
        """Check if the car has arrived."""
        return self.stepLeft == 0

    def nextRoad(self):
        """
        Determine the next road for the car.
        Returns the ID of the next road or -1 if no road change is needed.
        """
        if self.dirs[0][1] == 1 and len(self.dirs) != 1:
            return self.dirs[1][0]  # ID of next road
        return -1  # No need to change road

    def move(self):
        """Move the car to the next position."""
        self.stepLeft -= 1
        if self.dirs[0][1] == 1:
            del self.dirs[0]  # Move to next direction
        else:
            self.dirs[0] = (self.dirs[0][0], self.dirs[0][1] - 1)

class Simulation(object):
    """
    A simulation of cars moving through a map.
    """

    def __init__(self, startEndList, carMap):
        """
        Initialize the simulation with the list of car routes and the map.
        """
        self.carN = len(startEndList)
        self.cm = carMap
        self.cm.initialCars([startEndList[i][0] for i in range(self.carN)])

        self.cars = []
        for i in range(self.carN):
            self.cars.append(Car(i, self.cm.getDirection(startEndList[i][0], startEndList[i][1])))

        self.carCnt = self.carN
        self.tick = 0

    def run(self, delay, limit, sec=0.1):
        """
        Run the simulation.
        - `delay`: Whether to pause the simulation between ticks.
        - `limit`: The maximum number of ticks before stopping the simulation.
        - `sec`: The delay in seconds between each tick (default is 0.1).
        """
        while self.carCnt:
            if self.tick > limit:
                return (-1, -1)

            if delay:
                sleep(sec)

            self.tick += 1
            self.cm.updateTrafficLights(self.tick)

            for i in range(self.carN):
                self.moveCarRecursively(i)

        self.cm.clearAllCars()
        total_time = 0
        for i in range(self.carN):
            total_time += self.cars[i].timeStamp
            # Uncomment to print car travel times:
            # print("Car", i, "takes", self.cars[i].timeStamp, "ticks.")
        
        return total_time, float(total_time) / self.carN

    def makeAMove(self, i, nextRoad):
        """
        Move the car to the next road or along the current road.
        """
        if nextRoad == -1:
            return self.cm.move(i)
        return self.cm.moveTo(i, nextRoad, self.tick)

    def moveCarRecursively(self, i):
        """
        Move the car recursively until it reaches its destination or a block is encountered.
        """
        if self.cars[i].isArrived() or self.cars[i].timeStamp == self.tick:
            return

        self.cars[i].timeStamp = self.tick
        nextRoad = self.cars[i].nextRoad()
        state = self.makeAMove(i, nextRoad)

        if state[0] == CarMap.BLOCKED_BY_OTHER_CAR:
            # If blocked, try moving again after resolving the block
            self.moveCarRecursively(state[1])
            state = self.makeAMove(i, nextRoad)

        if state[0] == CarMap.SUCCESS:
            self.cars[i].move()
            if self.cars[i].isArrived():
                self.cm.remove(i)
                self.carCnt -= 1

if __name__ == '__main__':
    # Run the simulation with a simple car route
    Simulation([((7, 4), (10, 4))], CarMap('face')).run()
