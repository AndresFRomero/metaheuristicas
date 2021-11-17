# BRKGA: Biased Random Key Genertic Algotirhm for 2D Knapsack
# Andres F. Romero

# Libraries
import random

class BRKGA_Knapsack:

    # Problem Configuration
    iter = 2            # Generations
    discard = 0.7       # Percentage
    population = 20     # Number of initial solutions

    # Problem parameters
    items = {}
    width = {}
    height = {}

    def bestInsertion(self, edges:set, binWidth:int, binHeight:int, itemWidth:int, itemHeight: int):
        
        for i in edges:
            contact = 0
            x0, y0 = i
            x1 ,y1 = x0+itemWidth, y0+itemHeight

            if (x1 <= binWidth and y1 <= binHeight):
                
            


    def objFun(self, width:int, height:int, items:dict, itemOrder: list):

        edges = { (0,0) }

        for i in itemOrder:

        pass

    def randomSol(self, items: dict):
        totItems = []
        for i in items:
            for j in range(items[i]['copies']):
                if random.random() < 0.2: 
                    totItems.append( [i, round(items[i]['score']*random.random(),2)] )
                else:
                    totItems.append( [i, items[i]['score']] )
        
        totItems = sorted(totItems, key=lambda a: a[1], reverse=True)
        order = [i[0] for i in totItems]

        return { 
                'order': order,
                'scores': [i[1] for i in totItems],
                'objFun': self.objFun(self.width, self.height, self.items, order)
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

        return solutions
        
        
