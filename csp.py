#!/usr/bin/python

__author__ = 'mep'

import sys
import getopt
import pprint
import random

iterations = 1
MAX_WIDTH = 1000

calc_waste = lambda li: sum(map(lambda x: 1000-x, [sum(b) for b in li]))


def simple_solve(data):
    solution = []
    w = 0
    curr = []

    for i in data:
        if i + w >= MAX_WIDTH:
            solution.append(curr[:])
            curr[:] = []
            curr.append(i)
            w = i
        else:
            curr.append(i)
            w += i

    solution.append(curr)
    return solution


def greedy_solve(data):
    tmp_data = data[:]
    solution = []
    curr = []
    while len(tmp_data) > 0:
        curr[:] = []
        idx = random.randrange(0, len(tmp_data))
#        first = data[idx]
#        data.remove(idx)
        curr.append(tmp_data.pop(idx))
        flag = True
        while flag:
            tot = curr[0]
            for i in range(0, len(tmp_data)):
                # Find position of first item that fits
                if tot + tmp_data[i] > MAX_WIDTH:
                    break
            while sum(curr) + tmp_data[i] <= MAX_WIDTH:
                curr.append(tmp_data.pop(i))
            flag = False
            solution.append(curr)
            #and sum(curr) + tmp_data[0] <= MAX_WIDTH:
#            tot += data[0]
#            curr.append(tmp_data.pop())

#        solution.append(curr)
    pprint.pprint(solution)
    return solution

def optimize(dataset, strategy):
    best = len(dataset) * MAX_WIDTH # Would indicate every item goes into its own row
    solution = []

    for i in range(1, iterations+1):
        print "Run #" + str(i)
        l = []
        if strategy == "NONE":
            l = dataset
            tmp = simple_solve(dataset)
        elif strategy == "ASORT":
            l = sorted(dataset)
            tmp = simple_solve(sorted(dataset))
        elif strategy == "DSORT":
            l = list(reversed(sorted(dataset)))
            tmp = simple_solve(list(reversed(sorted(dataset))))
        elif strategy == "RANDOM":
            random.shuffle(dataset)
            l = dataset
            tmp = simple_solve(dataset)
        elif strategy == "GREEDY":
            tmp = greedy_solve(list(reversed(sorted(dataset))))

        #pprint.pprint(l)
        #pprint.pprint(tmp)
        waste = calc_waste(tmp)
        #print "Waste: " + str(waste)
        if waste < best:
            best = waste
            solution = tmp

    return solution


def main(argv):

    global iterations
    filename = 'orders.txt'
    strategy = 'GREEDY'

    try:
        opts, args = getopt.getopt(argv, 'i:n:s:', ['input=', 'numcount=', 'strategy='])
    except getopt.GetoptError:
            print "Invalid parameters"

    for opt, arg in opts:
        if opt in ('-i', '--input'):
            filename = arg
        if opt in ('-n', '--numcount'):
            iterations = int(arg)
        if opt in ('-s', '--strategy'):
            strategy = arg

    if filename == '':
        print "No input file given"
        exit()

    widths = [int(line.strip()) for line in open(filename) if line.strip().isdigit()]

    for i in range(len(widths)):
        if widths[i] > MAX_WIDTH:
            print "Invalid width in inputs"

    #pprint.pprint(widths)
    result = optimize(widths, strategy)

    print "Best solution: "
    #pprint.pprint(result)
    print "Number of cuts: " + str(len(result))
    print "Waste: " + str(calc_waste(result))

if __name__ == '__main__':
    main(sys.argv[1:])