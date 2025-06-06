# main.py

import sys
import pickle
from optparse import OptionParser
from _thread import start_new_thread
from random import randint

from layout import getLayout
from car import CarMap
from graphic import Graphic
from simulate import Simulation
from ga import Gene, GeneInfo
from generation import Generation


def parseArgs(argv):
    """
    Parse the command-line arguments.
    """
    parser = OptionParser()
    parser.add_option('-l', '--layout', dest='layout', type='str', default='single_cross')
    parser.add_option('-n', '--number', dest='number', type='int', default=10)
    parser.add_option('-z', '--zoom', dest='size', type='int', default=16)
    parser.add_option('-d', '--delay', dest='delay', type='float', default=0.2)
    parser.add_option('-g', '--generation', dest='generation', type='int', default=20)
    parser.add_option('-a', '--amount', dest='amount', type='int', default=20)
    parser.add_option('-s', '--save', dest='save', type='str', default='save.p')
    parser.add_option('-r', '--load', dest='load', type='str', default='')
    parser.add_option('--no_display', action='store_false', dest='display', default=True)
    parser.add_option('--no_simulate', action='store_false', dest='simulate', default=True)

    options, otherjunk = parser.parse_args(argv)
    if otherjunk:
        raise Exception('Command line input not understood: ' + str(otherjunk))

    arguments = {
        'layoutName': options.layout,
        'layout': getLayout(options.layout),
        'display': options.display,
        'simulate': options.simulate,
        'number': options.number,
        'size': options.size,
        'delay': options.delay,
        'generation': options.generation,
        'amount': options.amount,
        'save': options.save,
        'load': options.load,
    }

    if arguments['layout'] is None:
        raise Exception(f"The layout '{options.layout}' can't be found.")

    return arguments


class Result:
    def __init__(self, layout, cars):
        self.layout = layout
        self.cars = cars


def save(obj, filename):
    with open('saved/' + filename, 'wb') as f:
        pickle.dump(obj, f)


def load(filename):
    with open('saved/' + filename, 'rb') as f:
        return pickle.load(f)


def run():
    print(simulation.run(args['display'], 100000, args['delay']))


def randomStartEndPoint(number=5):
    pos = {}
    for _ in range(number):
        while True:
            r = randint(0, len(carmap.roads) - 1)
            i = randint(0, carmap.roads[r].getDistance() - 1)
            if (r, i) not in pos:
                pos[(r, i)] = carmap.roads[r].getPosByIndex(i)
                break

    result = []
    for ri, p in pos.items():
        while True:
            r = randint(0, len(carmap.roads) - 1)
            i = randint(0, carmap.roads[r].getDistance() - 1)
            if ri != (r, i):
                result.append((p, carmap.roads[r].getPosByIndex(i)))
                break

    return result


if __name__ == '__main__':
    """
    > python main.py
    """
    args = parseArgs(sys.argv[1:])

    if args['load'] == '':
        if args['simulate']:
            mapLayout = args['layout']
            carmap = CarMap(mapLayout, None)
            cars = randomStartEndPoint(args['number'])
            g = Generation(mapLayout, carmap, cars, args['amount'], args['generation'])
            results = g.run()

            print("Best in each generation:\n")
            for counter, r in enumerate(results[::2], start=1):
                a, s = r
                print(f"[{counter}] {a:.2f} {s}")

            print('\n-----------------------------------------------------------\n')
            print("Middle in each generation:\n")
            for counter, r in enumerate(results[1::2], start=1):
                a, s = r
                print(f"[{counter}] {a:.2f} {s}")

            save(Result(args['layoutName'], cars), args['save'])

        else:
            mapLayout = args['layout']
            gene = Gene(mapLayout.getTrafficLights())
            geneInfo = GeneInfo(gene)
            carmap = CarMap(mapLayout, geneInfo)
            cars = randomStartEndPoint(args['number'])
            simulation = Simulation(cars, carmap)

            app = Graphic(mapLayout.mapInfo, carmap.cars, carmap.trafficlights, args['size'])
            start_new_thread(run, ())
            app.run()

    else:
        r = load(args['load'])
        mapLayout = getLayout(r.layout)
        geneStr = input('Input Gene String: ')
        gene = Gene(mapLayout.getTrafficLights(), False, geneStr)
        geneInfo = GeneInfo(gene)
        carmap = CarMap(mapLayout, geneInfo)
        cars = r.cars
        simulation = Simulation(cars, carmap)

        if args['display']:
            app = Graphic(mapLayout.mapInfo, carmap.cars, carmap.trafficlights, args['size'])
            start_new_thread(run, ())
            app.run()
        else:
            run()
