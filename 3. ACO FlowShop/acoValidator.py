# Ant Colony Optimization Validator for FlowShop
import aco
import os
import time

def loadData(file : str):
    with open(file, 'r') as fp:
        problem = { 'timeMatrix' : {} }
        n = 1
        for line in fp:
            line = line.rstrip('\n')
            if n >= 4:
                times = line.replace("  ", " ").split(" ")
                for idx, time in enumerate(times):
                    problem['timeMatrix'][n-3,idx+1] = int(time)
            n += 1
    fp.close()
    problem['machines'] = [ i+1 for i in range(5)]
    problem['jobs'] = set([ i+1 for i in range(20)])

    return problem

for subdir, dirs, files in os.walk('./Tests'):
    for file in files:
        ACO = aco.AntColonyOptimization()
        strFile = os.path.join(subdir, file)
        problem = loadData(strFile)
        print(problem)
        start_time = time.time()
        route, makespan, deadtime = ACO.main(problem)
        print(file, makespan, round(time.time()-start_time,2) )