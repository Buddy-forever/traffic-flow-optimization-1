# ga.py

from random import randint


class Gene:
    """
    Represents a genetic configuration for traffic light durations.
    Can be generated randomly or from a gene string.
    """

    def __init__(self, trafficInfo, randomGenerate=True, geneStr=""):
        self.geneStr = ""
        self.geneLen = 0
        self.trafficInfo = trafficInfo
        self.matched = {}
        self.roadToLight = {}
        self.roadInfo = {}
        self.lightInfo = {}

        if randomGenerate:
            self.buildUpGene()
        else:
            self.buildFromStr(geneStr)

    def buildUpGene(self):
        """
        Builds a gene string with random durations for traffic lights.
        """
        for trafficLight, intersections in self.trafficInfo:
            self.geneLen += len(intersections)
            lightlist = []

            for _ in range(len(intersections)):
                duration = randint(2, 20)
                lightlist.append(duration)
                self.geneStr += f"{duration:02d}"

            self.lightInfo[trafficLight] = lightlist
            self.roadInfo[trafficLight] = intersections

            for road in intersections:
                self.roadToLight[road] = trafficLight

    def buildFromStr(self, geneStr):
        """
        Builds the gene information from a predefined gene string.
        """
        self.geneStr = geneStr
        index = 0

        for trafficLight, intersections in self.trafficInfo:
            self.geneLen += len(intersections)
            lightlist = []

            for _ in range(len(intersections)):
                duration = int(geneStr[index * 2 : index * 2 + 2])
                lightlist.append(duration)
                index += 1

            self.lightInfo[trafficLight] = lightlist
            self.roadInfo[trafficLight] = intersections

            for road in intersections:
                self.roadToLight[road] = trafficLight


class GeneInfo:
    """
    Determines if a light is green for a road at a given simulation tick.
    """

    def __init__(self, gene):
        self.gene = gene

    def isGreen(self, road, tick):
        intersection = self.gene.roadToLight[road]
        roadlist = self.gene.roadInfo[intersection]
        lightlist = self.gene.lightInfo[intersection]
        cycle = sum(lightlist)
        tick = tick % cycle

        for i in range(len(roadlist)):
            if tick >= lightlist[i]:
                tick -= lightlist[i]
            elif road == roadlist[i]:
                return True
            else:
                return False

        return False


class GeneEvolve:
    """
    Handles the evolution logic for two genes.
    """

    @classmethod
    def evolve(cls, g1, g2, mutateRate=0.2):
        """
        Combines and mutates two parent genes to create a new gene.
        """
        newGen = cls.merge(g1, g2)
        geneStr = cls.mutate(newGen, mutateRate)
        return Gene(g1.trafficInfo, randomGenerate=False, geneStr=geneStr)

    @classmethod
    def merge(cls, g1, g2):
        """
        Merges two gene strings by selecting half of their traits.
        """
        newGen = ""
        genLen = len(g1.geneStr)
        geneStrs = [g1.geneStr, g2.geneStr]

        for i in range(genLen // 2):
            selected = randint(0, 1)
            newGen += geneStrs[selected][i * 2 : i * 2 + 2]

        return newGen

    @classmethod
    def mutate(cls, geneStr, mutateRate):
        """
        Applies mutations to a gene string by randomly changing durations.
        """
        num_mutations = randint(0, int((len(geneStr) / 2) * mutateRate))
        geneList = list(geneStr)

        for _ in range(num_mutations):
            pos = randint(0, (len(geneStr) // 2) - 1)
            new_val = f"{randint(2, 20):02d}"
            geneList[pos * 2 : pos * 2 + 2] = list(new_val)

        return ''.join(geneList)
