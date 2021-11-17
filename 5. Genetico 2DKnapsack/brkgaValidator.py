# BRKGA: Biased Random Key Genertic Algotirhm for 2D Knapsack

import brkga
import os
import time

def loadData(file : str):
    with open(file, 'r') as fp:
        problem = { 'width' : 0, 'height': 0, 'numberOfItems':0, 'items': {} }
        n = 1
        for line in fp:
            line = line.rstrip('\n')
            if n == 1:
                problem['numberOfItems'] = int(line)
            elif n == 2:
                line = line.split(" ")
                problem['width'] = int(line[0])
                problem['height'] = int(line[1])
            elif (n>=3 and n<= problem['numberOfItems']+2):
                itemData = line.split(" ")
                itemData = [ int(i) for i in itemData]
                problem['items'][itemData[0]] = {
                    'width': itemData[1],
                    'height': itemData[2],
                    'demand': itemData[3],
                    'copies': itemData[4],
                    'profit': itemData[5]
                }
            else:
                pass
            n += 1
    fp.close()

    return problem

BRKGA = brkga.BRKGA_Knapsack()

file = './Tests/NGCUT/NGCUT2.ins2D'

for _ in range(30):
    problem = loadData(file)
    start_time = time.time()
    sol = BRKGA.main(problem)
    print(file, sol, round(time.time()-start_time, 5))