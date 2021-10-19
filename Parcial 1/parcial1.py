'''
Proyecto Metaheristicas
Andres Felipe Romero Silva
201515617
'''

# Libraries
from math import cos
from scipy.spatial import distance
import random

# Data
students = {
    'Andres' : [0, 8, 2, 10, 5, 9],
    'Ariadna' : [0, 1, 6, 5, 3, 5],
    'Carlos' : [5, 5, 2, 10, 1, 4],
    'Cristian' : [10, 1, 3, 10, 9, 4],
    'JuanB': [0, 4, 1, 8, 1, 5],
    'JuanC' : [1, 9, 10, 3, 6, 0],
    'Sebastian' : [6, 6, 0, 8, 10, 4],
    'Sofia': [2, 3, 1, 10, 5, 9],
    'Javier': [6, 8, 2, 8, 6, 0]
}

# Pre-process
dM = {} # Distance matrix
for i in students:
    for j in students:
        dM[i,j] = distance.euclidean(students[i], students[j])

# Constructive Heuristic: Elimination
def objFun(group:set, dM: dict):
    FO = 0
    for i in group:
        for j in group:
            FO += dM[i,j]
    return FO/len(group) # mean FO 

def formalElimination(group:set, dM: dict, strong:bool):
    # one single elimination.
    iniFO = 0
    iniGroup = group
    iniEl = '-1'

    for i in group:
        newGroup = group.difference(set([i]))
        newFO = objFun(newGroup, dM)
        if(newFO > iniFO):
            iniGroup = newGroup
            iniFO = newFO
            iniEl = i

    if strong:
        return iniGroup
    else:
        return iniEl

def randomElimination(group:set):
    # one single elimination
    group.remove(random.sample(group,1)[0])

def localSearch(students:dict, group:set, dM:dict, ObjFun: float):
    # Inits
    improve = True
    improveFO = ObjFun
    improveGroup = group

    count = 0
    while improve:
        removeCandidate = formalElimination(improveGroup, dM, False)
        candidateGroup = improveGroup # Init
        improve = False # exit while

        for i in set(students.keys()).difference(improveGroup):
            test = improveGroup.difference(set([removeCandidate]))
            newFO = objFun(test, dM)
            if newFO > improveFO:
                improveFO = newFO
                candidateGroup = test
                improve = True

        improveGroup = candidateGroup
    count += 1
    return improveFO, improveGroup

# Just the pseudo-randomized heuristic
def constructive(students:dict, dM:dict, n:int, alpha: float):
    group = set(students.keys())

    while len(group)>n:
        if random.random() < alpha:
            randomElimination(group)
        else:
            group = formalElimination(group, dM, True)

    return objFun(group, dM), group 

print('Pseudo-Random-Heuristic', constructive(students, dM, 5, 0.2)) 

# Metaheuristic implementation
def GRASP(students:dict, dM:dict, n:int, alpha: float, maxIters: int):

    bestSol = (0,set())

    for _ in range(maxIters):
        objFun, solution = constructive(students, dM, n, alpha)
        objFun, solution = localSearch(students, solution, dM, objFun)

        if objFun > bestSol[0]:
            bestSol = (objFun, solution)

    return bestSol

print('GRASP Procedure', GRASP(students, dM, 5, 0.2, 200))