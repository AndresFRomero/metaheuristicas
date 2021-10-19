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

def formalElimination(group:set, dM: dict):
    # one single elimination.
    iniFO = objFun(group, dM)
    iniGroup = group

    for i in group:
        newGroup = group.difference(set(i))
        newFO = objFun(newGroup, dM)
        if(newFO > iniFO):
            iniGroup = newGroup
            iniFO = newFO

    return iniGroup

def randomElimination(group:set):
    # one single elimination
    group.remove(random.sample(group,1)[0])

def constructive(students:dict, dM:dict, n:int, alpha: float):
    group = set(students.keys())

    while len(group)>n:
        if random.random() < alpha:
            randomElimination(group)
        else:
            group = formalElimination(group, dM)

    return objFun(group, dM), group 

# Just the pseudo-randomized heuristic
print('Pseudo-Random-Heuristic', constructive(students, dM, 5, 0.2)) 

# Metaheuristic implementation