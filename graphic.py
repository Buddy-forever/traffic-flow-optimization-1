#!/usr/bin/env python

from tkinter import *
from game import Info

class Graphic:
    def __init__(self, graphInfo, carList, trafficlightList, gridsize=10):
        """Initialize the graphic window with traffic flow visualization."""
        self.master = Tk()
        self.master.title("Traffic Flow Optimization")
        
        # Create frames for the layout
        self.frame1 = Frame(self.master)
        self.frame1.pack()
        self.frame2 = Frame(self.master)
        self.frame2.pack()

        # Initialize graph dimensions and data
        wid = graphInfo.width
        hei = graphInfo.height
        data = [[0] * hei for _ in range(wid)]

        self.gridSize = gridsize
        self.width = wid * gridsize
        self.height = hei * gridsize
        self.cars = carList
        self.trafficlights = trafficlightList

        # Create canvas for drawing
        self.canvas = Canvas(self.frame1, width=self.width, height=self.height)
        self.canvas.pack()

        # Initialize data from the provided graph info
        self.initDataFromInfo(graphInfo, data)
        self.drawRoadAndBuilding(data, wid, hei)

        # Add buttons for stop/play and quit
        self.stopButton = Button(self.frame2, text="Stop/Play", command=self.stopOrContinue)
        self.stopButton.grid(row=0, column=0)

        self.quitButton = Button(self.frame2, text="Quit", command=self.quit)
        self.quitButton.grid(row=0, column=1)

        self.isStop = False
        self.graphicItem = []
        self.graphicItemShadow = []
        self.graphicItemShadow2 = []

    def run(self, fps=20):
        """Start the main event loop with specified frames per second."""
        self.fps = fps
        self.frameTime = 1000 / self.fps
        self.frame1.after(self.frameTime, self.updateElement)
        self.master.mainloop()

    def initDataFromInfo(self, graphInfo, data):
        """Initialize data array based on the provided graph information."""
        for x in range(graphInfo.width):
            for y in range(graphInfo.height):
                dataType = graphInfo.data[x][y][0]
                if dataType == Info.FIELD:
                    data[x][y] = 0
                elif dataType == Info.CROSSROAD:
                    data[x][y] = 3
                elif dataType == Info.INTERSECTION:
                    data[x][y] = 2
                elif dataType == Info.ROAD:
                    data[x][y] = 1

    def drawRoadAndBuilding(self, data, wid, hei):
        """Draw roads and buildings based on the provided data."""
        gridsize = self.gridSize
        for x in range(wid):
            for y in range(hei):
                pos_x = x * gridsize
                pos_y = y * gridsize
                if data[x][y] == 0:
                    self.canvas.create_rectangle(pos_x, pos_y, pos_x+gridsize, pos_y+gridsize, fill="#eee", width=0)
                elif data[x][y] == 2:
                    self.canvas.create_rectangle(pos_x, pos_y, pos_x+gridsize, pos_y+gridsize, fill="#333", width=0)
                    self.canvas.create_line(pos_x, pos_y, pos_x+gridsize, pos_y+gridsize, fill="#b93")
                    self.canvas.create_line(pos_x+gridsize, pos_y, pos_x, pos_y+gridsize, fill="#b93")
                elif data[x][y] == 3:
                    self.canvas.create_rectangle(pos_x, pos_y, pos_x+gridsize, pos_y+gridsize, fill="#222", width=0)
                else:
                    self.canvas.create_rectangle(pos_x, pos_y, pos_x+gridsize, pos_y+gridsize, fill="#333", width=0)

    def updateElement(self):
        """Update the elements on the canvas (traffic lights, cars, etc.)."""
        gridsize = self.gridSize

        # Clear previous shadow items
        for item in self.graphicItemShadow2:
            self.canvas.delete(item)

        self.graphicItemShadow2 = self.graphicItemShadow
        self.graphicItemShadow = self.graphicItem
        self.graphicItem = []

        # Update traffic lights
        for light in self.trafficlights:
            x, y = light.pos
            pos_x = x * gridsize
            pos_y = y * gridsize
            colorToDraw = "#f00" if not light.isGreen else "#0c0"
            coords = [pos_x+1, pos_y+1, pos_x+gridsize-1, pos_y+gridsize-1]
            self.graphicItem.append(self.canvas.create_rectangle(coords, fill=colorToDraw))

        # Update shadow items
        for item in self.graphicItemShadow2:
            self.canvas.itemconfig(item, fill="#433")
        for item in self.graphicItemShadow:
            self.canvas.itemconfig(item, fill="#543")

        # Update cars
        for car in self.cars:
            if not car.display:
                continue
            x, y = car.pos
            pos_x = x * gridsize
            pos_y = y * gridsize

            if car.way == "N":
                coords = [pos_x+gridsize/2, pos_y+2, pos_x+2, pos_y+gridsize-2, pos_x+gridsize/2, pos_y+2+gridsize/2, pos_x+gridsize-2, pos_y+gridsize-2]
            elif car.way == "W":
                coords = [pos_x+2, pos_y+gridsize/2, pos_x+gridsize-2, pos_y+gridsize-2, pos_x+2+gridsize/2, pos_y+gridsize/2, pos_x+gridsize-2, pos_y+2]
            elif car.way == "S":
                coords = [pos_x+gridsize/2, pos_y+gridsize-2, pos_x+gridsize-2, pos_y+2, pos_x+gridsize/2, pos_y-2+gridsize/2, pos_x+2, pos_y+2]
            else:
                coords = [pos_x+gridsize-2, pos_y+gridsize/2, pos_x+2, pos_y+2, pos_x-2+gridsize/2, pos_y+gridsize/2, pos_x+2, pos_y+gridsize-2]
            self.graphicItem.append(self.canvas.create_polygon(coords, fill="#f96"))

        # Update at the next frame
        if not self.isStop:
            self.frame1.after(self.frameTime, self.updateElement)

    def stopOrContinue(self):
        """Toggle between stopping and continuing the animation."""
        self.isStop = not self.isStop
        if not self.isStop:
            self.frame1.after(self.frameTime, self.updateElement)

    def quit(self):
        """Quit the program."""
        print("Program End!")
        self.master.destroy()
