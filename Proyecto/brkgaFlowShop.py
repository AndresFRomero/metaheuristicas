# Proyecto Metaheuristicas
# Andres F. Romero
# Sebastián Bueno

import random

class tppConstructive:
    # Initializate params
    markets = set()
    products = list
    cost_matrix = {}
    offer_section = {}

    # Ram Costs
    purchaseCosts = dict()
    aproxTravelCosts = dict()
    robustTravelCosts = dict()

    # Best Solution
    bestRoute = []
    bestPurchases = []
    bestObjFun = float('inf')
    
    def loadData(self, data):
        self.markets = set([ i+1 for i in range(data['dimension'])])
        self.products = [ i+1 for i in range(data['products_dimension'])]
        self.cost_matrix = data['cost_matrix']
        self.offer_section = data['offer_section']

    def aproxTravelCost(self, cM:dict, markets: set):

        if tuple(sorted([i for i in markets])) in self.aproxTravelCosts:
            return self.aproxTravelCosts[tuple(sorted([i for i in markets]))]
        else:
            suma = 0
            for i in cM:
                if (i[0] in markets and i[1] in markets):
                    suma += cM[i]

            finalCost =  suma/(len(markets) - 1)  
            self.aproxTravelCosts[tuple(sorted([i for i in markets])) ] = finalCost

            return finalCost

    def tsp(self, cM:dict, markets: set, origin:int = 1):
        visited = set([origin])
        unvisited = markets.difference(visited)

        # Route initialization
        route = [origin]

        # Algorithm complexity O(logN); N: nodes (packages)
        while len(unvisited) > 0:
            # Solution initialization
            nearest = float("inf")
            nextnode = "-1"

            for j in unvisited:
                test = cM[route[-1], j]
                if test < nearest:
                    nearest = test
                    nextnode = j

            route.append(nextnode)
            visited.add(nextnode)
            unvisited.discard(nextnode)

        route.append(origin)
        return route

    def routeCost(self, cM: dict, route: list) -> float:
        return sum([cM[(route[i], route[i + 1])] for i in range(len(route) - 1)])

    def _2optSwap(self, route: list, i: int, k: int) -> list:
        firstPart = route[0:i]
        secondPart = route[i:k + 1]
        thirdPart = route[k + 1:len(route)]
        return firstPart + secondPart[::-1] + thirdPart

    def simple2opt(self, cM: dict, route: list) -> list:

        n = len(route) # Nodes

        # Solution Initialization
        route = route
        bestRoute = route
        bestCost = self.routeCost(cM, bestRoute)

        improvement = True
        while improvement == True:
            improvement = False
            for i in range(1, n - 1):
                for j in range(i + 1, n-1):
                    newRoute = self._2optSwap(route, i, j)
                    newCost = self.routeCost(cM, newRoute)

                    if newCost < bestCost:
                        bestRoute = newRoute
                        bestCost = newCost
                        improvement = True

                route = bestRoute

        return bestRoute

    def whereToBuy(self, route:list, products:list, cM: dict, offers: dict):
        
        whereToBuy = []
        factible = True
        buyCost = 0

        for i in products:
            buyIn = -1
            actualCost = float('inf')
            for j in route:
                try:
                    testCost = offers[j][i]
                    if testCost<actualCost:
                        actualCost = testCost
                        buyIn = j
                except:
                    pass
            if(buyIn == -1):
                factible = False
                break

            whereToBuy.append(buyIn)
            buyCost+=actualCost

        return whereToBuy, buyCost, factible

    def bestElimination(self, route:list, products:list, cM:dict, offers:dict):
        
        bestFO = float('inf')
        bestRoute = route
        bestWhereToBuy = self.whereToBuy(route,products,cM,offers)[0]
        bestRemove = '-1'

        for i in route[1:-1]:
            newRoute = route.copy()
            newRoute.remove(i)

            whereToBuy, buyCost, factible = self.whereToBuy(newRoute, products, cM, offers)
            routeCost = self.routeCost(cM, newRoute)
            if factible:
                newFO = buyCost + routeCost
                if newFO<bestFO:
                    bestFO = newFO
                    bestRoute = newRoute
                    bestWhereToBuy = whereToBuy
                    bestRemove = i
                    
        return bestRoute, bestWhereToBuy, bestFO

    def purchaseCost(self, markets:set, offerSection:dict, products:list):
        
        if tuple(sorted([i for i in markets]))  in self.purchaseCosts:
            return self.purchaseCosts[tuple(sorted([i for i in markets]))]['cost']
        else:
            costs = { i:[float('inf'),'-1'] for i in products }

            for i in markets:
                for j in offerSection[i]:
                    if costs[j][0] > offerSection[i][j]:
                        costs[j][0] = offerSection[i][j]
                        costs[j][1] = i
            
            finalCosts = sum([ costs[i][0] for i in costs ])
            self.purchaseCosts[tuple(sorted([i for i in markets]))] = { 'cost': finalCosts, 'where':costs }
            
            return finalCosts

    def randomCromosome(self, markets:set):
        cromosome = { i: random.random() for i in markets if i != 1 } # cromosome is the orden of deletion of markets
        sortedCromosome = sorted([ (cromosome[i],i) for i in cromosome ])
        return sortedCromosome

    def posibleRemove(self, markets:set, products:list, offerSection: dict):
        
        offers = set()
        condition = False

        for i in markets:
            for j in offerSection[i].keys():
                offers.add(j)
                if offers == set(products):
                    return True

        return condition

    def cromosomeDecoder(self, cromosome:list, markets:set, products:list, cM:dict, offerSection: dict):

        actualTravelCost = float('inf')
        actualPurchaseCost = float('inf')
        actualFO = actualPurchaseCost + actualTravelCost

        marketsVisited = markets.copy()

        for i in cromosome:
            testSet = marketsVisited.copy()
            testSet.remove(i[1])

            newTravelCost = self.aproxTravelCost(cM, testSet)
            posibleRemove = self.posibleRemove(testSet, products, offerSection)

            # Decition of decoder
            if posibleRemove:
                newPurshaseCost = self.purchaseCost(testSet, offerSection, products)
                if newPurshaseCost + newTravelCost < actualFO:
                    marketsVisited.remove(i[1])
                    actualPurchaseCost = newPurshaseCost
                    actualTravelCost = newTravelCost
                    actualFO = actualTravelCost + actualPurchaseCost
        
        return marketsVisited

    def createRoute(self, cM:dict, products:list, offers:dict, markets:set):
        # Nearest Neighboor TSP
        marketRoute = self.tsp(cM, markets, 1)
        # 2OPT improvement
        marketRoute = self.simple2opt(cM, marketRoute)
        
        whereToBuy = []
        for i in products:
            whereToBuy.append(self.purchaseCosts[tuple(sorted(markets))]['where'][i][1])

        return marketRoute, whereToBuy

    def main(self, data):
        self.loadData(data)

        for _ in range(1000):
            randCrom = self.randomCromosome(self.markets)
            marketsVisited = self.cromosomeDecoder(randCrom, self.markets, self.products, self.cost_matrix, self.offer_section)

            route, whereToBuy = self.createRoute(self.cost_matrix, self.products, self.offer_section, marketsVisited)
            routeCost =  self.routeCost(self.cost_matrix, route)
            purchaseCost = self.purchaseCosts[tuple(sorted([i for i in marketsVisited]))]['cost']

            if routeCost + purchaseCost < self.bestObjFun:
                self.bestObjFun = routeCost + purchaseCost
                self.bestRoute = route
                self.bestPurchases = whereToBuy

        return self.bestRoute, self.bestPurchases, self.bestObjFun
        # ONLY CONSTRUCTIVE - HEURISTIC

        # # Nearest Neighboor TSP
        # marketRoute = self.tsp(self.cost_matrix, self.markets, 1)

        # # 2OPT improvement
        # marketRoute = self.simple2opt(self.cost_matrix, marketRoute)
        # whereToBuy = self.whereToBuy(marketRoute, self.products, self.cost_matrix, self.offer_section)[0]

        # improve = True
        # objFun = self.routeCost(self.cost_matrix, marketRoute) + self.whereToBuy(marketRoute,self.products, self.cost_matrix, self.offer_section)[1]
        
        # while improve:
        #     improve = False
        #     newRoute, newWhereToBuy, newFO = self.bestElimination(marketRoute, self.products, self.cost_matrix, self.offer_section)

        #     if newFO < objFun:
        #         marketRoute = newRoute
        #         whereToBuy = newWhereToBuy
        #         objFun = newFO
        #         improve = True

        # return marketRoute, whereToBuy, objFun