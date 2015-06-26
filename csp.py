#!/usr/bin/python

__author__ = 'mep'

import sys
import getopt
import pprint
import random

# Default values for global settings
iterations = 1
MAX_WIDTH = 1000

calc_waste = lambda li: sum(map(lambda x: MAX_WIDTH-x, [sum(b) for b in li]))
values_only = lambda li: [x[1] for x in li]


def simple_solve(data):
    solution = []
    curr = []
    tmp_data = data[:]

    while len(tmp_data) > 0:
        while tmp_data[0] + sum(curr) <= MAX_WIDTH:
            curr.append(tmp_data.pop(0))
            if len(tmp_data) == 0:
                break
        solution.append(curr[:])
        curr[:] = []

    return solution


def greedy_solve(data):
    tmp_data = data[:]
    solution = []
    curr = []
    while len(tmp_data) > 0:
        curr[:] = []
        # Randomly select an item from the list and move to first row
        idx = random.randrange(0, len(tmp_data))
        curr.append(tmp_data.pop(idx))
        for item in tmp_data:
            if item[1] + sum(values_only(curr)) <= MAX_WIDTH:
                curr.append(item)
        tmp_data[:] = [x for x in tmp_data if x not in curr]
        solution.append(values_only(curr))
    return solution


def match_solve(data):
    solution = []
    tmp_data = data[:]
    tmp_data2 = []

    while tmp_data:
        item = tmp_data[0]
        for i in range(1, len(tmp_data)):
            if item[1] + tmp_data[i][1] >= MAX_WIDTH*0.95 and item[1] + tmp_data[i][1] <= MAX_WIDTH:
                solution.append([item[1], tmp_data[i][1]])
                tmp_data2.append(item)
                tmp_data2.append(tmp_data[i])
                del tmp_data[i]
                break
        del tmp_data[0]

    tmp_data[:] = [x for x in data if x not in tmp_data2]

    while tmp_data:
        item1 = tmp_data[0]
        for i in range(1, len(tmp_data)):
            item2 = tmp_data[i]
            for j in range(i, len(tmp_data)):
                if item1[1] + item2[1] + tmp_data[j][1] >= MAX_WIDTH*0.95 and \
                    item1[1] + item2[1] + tmp_data[j][1] <= MAX_WIDTH:
                    solution.append([item1[1], item2[1], tmp_data[j][1]])
                    tmp_data2.append(item1)
                    tmp_data2.append(item2)
                    tmp_data2.append(tmp_data[j])
                    del tmp_data[j]
                    del tmp_data[i]
        del tmp_data[0]

    tmp_data[:] = [x for x in data if x not in tmp_data2]

    random.shuffle(tmp_data)
    return solution + greedy_solve(tmp_data)

def optimize(dataset, strategy):
    best = len(dataset) * MAX_WIDTH # Would indicate every item goes into its own row, i.e. worst case
    solution = []

    for i in range(1, iterations+1):
        if strategy == "NONE":
            # Just split the items into rows
            tmp = simple_solve(values_only(dataset))
        elif strategy == "ASORT":
            # Sort ascending, then split
            tmp = simple_solve(sorted(values_only(dataset)))
        elif strategy == "DSORT":
            # Sort descending, then split
            tmp = simple_solve(list(reversed(sorted(values_only(dataset)))))
        elif strategy == "RANDOM":
            # Randomise the items, then split
            random.shuffle(dataset)
            tmp = simple_solve(values_only(dataset))
        elif strategy == "GREEDY":
            # Randomly select first item for each row, go through list to
            # find items matching
            tmp = greedy_solve(dataset)
        elif strategy == "GREEDYSORT":
            # Same as greedy, but sort list descending first
            tmp = greedy_solve(list(reversed(sorted(dataset))))
        elif strategy == "GREEDYRANDOM":
            # Same as greedy, but randomize list first
            random.shuffle(dataset)
            tmp = greedy_solve(dataset)
        elif strategy == "GREEDYMATCH":
            # First tries to find pairs and triplets that are exactly
            # MAX_WIDTH and only after that runs greedy strategy on
            # the rest.
            tmp = match_solve(dataset)

        #pprint.pprint(tmp)
        waste = calc_waste(tmp)
        if waste < best:
            best = waste
            solution = tmp

    return solution


def main(argv):

    global iterations
    filename = '1000orders.txt'
    strategy = 'GREEDYMATCH'

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

    widths = []
    with open(filename) as f:
        for num, line in enumerate(f, 1):
            widths.append((num, int(line)))

    for i in range(len(widths)):
        if widths[i][1] > MAX_WIDTH:
            print "Invalid width in inputs"

    print "Theoretical best solution: " + str(sum(values_only(widths))/1000+1) + " rows."
    result = optimize(widths, strategy)

    print "Best solution: "
    pprint.pprint(result)
    print "Number of rows: " + str(len(result))
    print "Waste: " + str(calc_waste(result))

if __name__ == '__main__':
    main(sys.argv[1:])