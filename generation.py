# generation.py

from random import randint
from simulate import Simulation
from ga import Gene, GeneInfo, GeneEvolve


class Generation:
    """
    Handles the evolution of traffic light genes over multiple generations.
    """

    def __init__(self, mapLayout, carmap, cars, geneNumber, roundNumber):
        self.mapLayout = mapLayout
        self.carmap = carmap
        self.cars = cars
        self.geneNumber = geneNumber
        self.roundNumber = roundNumber
        self.genes = []
        self.results = []
        self.initialFirstGenes()

    def initialFirstGenes(self):
        """
        Randomly generates the initial set of genes.
        """
        for _ in range(self.geneNumber):
            self.genes.append(Gene(self.mapLayout.getTrafficLights()))

    def run(self):
        """
        Runs the evolutionary process across multiple generations.
        """
        for i in range(self.roundNumber):
            result = []
            print(f'Generation {i + 1}:')

            for g in self.genes:
                print(f'\tGene String {g.geneStr}')
                self.carmap.updateGeneInfo(GeneInfo(g))
                simulation = Simulation(self.cars, self.carmap)
                total, average = simulation.run(False, 10000)
                print(f'\tTotal: {total} Average: {average}\n')

                if average == -1:
                    self.carmap.clearAllCars()
                    continue

                result.append((average, g))

            # FIX REQUIRED: Sort by average because Gene objects are not directly comparable
            result.sort(key=lambda x: x[0])

            selected = result[: (self.geneNumber // 2 + 1)]
            self.addResults(selected)
            self.evolve(selected)

        return self.results

    def evolve(self, result):
        """
        Produces a new generation from top-performing genes.
        """
        newGenes = []
        length = len(result) - 1

        for _ in range(self.geneNumber):
            g1, g2 = randint(0, length), randint(0, length)
            newGene = GeneEvolve.evolve(result[g1][1], result[g2][1])
            newGenes.append(newGene)

        self.genes = newGenes

    def addResults(self, result):
        """
        Stores the best and worst performing gene strings of each generation.
        """
        self.results.append((result[0][0], result[0][1].geneStr))      # Best
        self.results.append((result[-1][0], result[-1][1].geneStr))    # Worst
