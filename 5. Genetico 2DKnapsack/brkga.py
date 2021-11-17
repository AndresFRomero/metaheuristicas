# BRKGA: Biased Random Key Genertic Algotirhm for 2D Knapsack
# Andres F. Romero

# Libraries
import random
import numpy as np

class BRKGA_Knapsack:

    # Problem Configuration
    iter = 10            # Generations
    discard = 0.5       # Percentage
    population = 2000     # Number of initial solutions
    alpha = 0.5

    # Problem parameters
    items = {}
    width = 0
    height = 0

    # Memory
    bestFO = 0
    bestOrder = []
    itemsUsed = []
    solutions = {}
    
    def bestInsertion(self, edges:list, binWidth:int, binHeight:int, itemWidth:int, itemHeight: int):
        
        bestImprove = - 999999
        bestNewEdges = edges.copy()

        for idx, value in enumerate(edges):
            x0, y0 = value
            x1 ,y1 = x0+itemWidth, y0+itemHeight
            edgesCopy = edges.copy()
            newEdges = []
            
            if (x1 <= binWidth and y1 <= binHeight):
                contacto = 0
                wasteX = 0
                wasteY = 0

                if y0 == 0:
                    contacto += itemWidth
                if x0 == 0:
                    contacto += itemHeight
                
                # First Insertion
                if len(edges) == 1:
                    newEdges.append( [x0,y1] )
                    newEdges.append( [x1,y0] )

                elif idx > 0:
                    wasteY = y1 - edges[idx-1][1]
                    if wasteY < 0:
                        newEdges.append( [x0,y1] )
                        wasteY = 0
                    if wasteY > 0:
                        edgesCopy[idx-1][1] = y1

                elif idx < len(edges)-1:
                    wasteX = x1 - edges[idx+1][0]
                    if wasteX < 0:
                        newEdges.append( [x1,y0] )
                    if wasteY > 0:
                        edgesCopy[idx+1][0] = x1

                improveTest = contacto - wasteY - wasteX

                if  improveTest > bestImprove:
                    del edgesCopy[idx]
                    bestImprove = improveTest
                    bestNewEdges = sorted( edgesCopy+newEdges, key = lambda tup: tup[0])

        return bestNewEdges, bestImprove

    def objFun(self, width:int, height:int, items:dict, itemOrder: list):

        edges = [ [0,0] ]
        profit = 0
        itemsUsed = []

        for i in itemOrder:
            edges , posible = self.bestInsertion(edges, width, height, items[i]['width'], items[i]['height'])
            if posible == - 999999:
                pass
            else:
                profit += items[i]['profit']
                itemsUsed.append(i)

        return profit, itemsUsed

    def randomSol(self, items: dict):
        totItems = []
        for i in items:
            for j in range(items[i]['copies']):
                if random.random() < self.alpha: 
                    totItems.append( [i, round(items[i]['score']*random.random(),2)] )
                else:
                    totItems.append( [i, items[i]['score']] )

        scores = [i[1] for i in totItems]

        totItems = sorted(totItems, key=lambda a: a[1], reverse=True)
        order = [i[0] for i in totItems]

        if tuple(order) in self.solutions:
            objFun = self.solutions[tuple(order)]['objFun']
            itemsUsed = self.solutions[tuple(order)]['itemsUsed']
        else:
            objFun, itemsUsed = self.objFun(self.width, self.height, self.items, order)
            self.solutions[tuple(order)] = { 'objFun': objFun, 'itemsUsed': itemsUsed}

        if objFun > self.bestFO:
            self.bestFO = objFun
            self.bestOrder = order
            self.itemsUsed = itemsUsed

        return { 
                'order': order,
                'scores': scores,
                'objFun': objFun,
                'itemsUsed' : itemsUsed
            }

    def cross(self, sol1, sol2, items:dict):

        scores = list(np.average( np.array([sol1['scores'], sol2['scores']]), axis = 0))

        totItems = []
        idx = 0
        for i in items:
            for j in range(items[i]['copies']):
                totItems.append( [i, scores[idx]] )
                idx += 1

        totItems = sorted(totItems, key=lambda a: a[1], reverse=True)
        order = [i[0] for i in totItems]
        
        if tuple(order) in self.solutions:
            objFun = self.solutions[tuple(order)]['objFun']
            itemsUsed = self.solutions[tuple(order)]['itemsUsed']
        else:
            objFun, itemsUsed = self.objFun(self.width, self.height, self.items, order)
            self.solutions[tuple(order)] = { 'objFun': objFun, 'itemsUsed': itemsUsed}

        if objFun > self.bestFO:
            self.bestFO = objFun
            self.bestOrder = order
            self.itemsUsed = itemsUsed

        return { 
                'order': order,
                'scores': scores,
                'objFun': objFun,
                'itemsUsed' : itemsUsed
            }

    def main(self, data:dict):

        # rewrite params
        self.items = data['items']
        self.width = data['width']
        self.height = data['height']

        # score calculation
        for i in self.items:
            self.items[i]['score'] = round(self.items[i]['profit']/(self.items[i]['width']*self.items[i]['height']),2)

        # InitialMix
        solutions = []
        while len(solutions) < self.population:
            solutions.append( self.randomSol(self.items) )

        for _ in range(self.iter):
            # Discard
            half = int(self.population*self.discard)
            solutions = sorted(solutions, key=lambda x: x['objFun'], reverse=True)[:half]

            # Cross
            def pop_random(lst):
                idx = random.randrange(0, len(lst))
                selected = lst[idx]
                del lst[idx]
                return selected
            
            # New Mix
            newSolutions = []
            while len(solutions) > 1:
                rand1 = pop_random(solutions)
                rand2 = pop_random(solutions)
                newSolutions.append(self.cross(rand1,rand2, self.items))
            
            solutions = newSolutions

        return self.bestFO, self.bestOrder, self.itemsUsed
        