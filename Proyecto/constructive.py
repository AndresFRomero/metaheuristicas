# Proyecto Metaheuristicas
# Andres F. Romero
# Sebastián Bueno

class tppConstructive:
    # Initializate params
    markets = set()
    products = list
    cost_matrix = {}
    offer_section = {}

    def loadData(self, data):
        self.markets = set([ i+1 for i in range(data['dimension'])])
        self.products = [ i+1 for i in range(data['products_dimension'])]
        self.cost_matrix = data['cost_matrix']
        self.offer_section = data['offer_section']

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
                for j in range(i + 1, n):
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

    def main(self, data):
        self.loadData(data)

        # Nearest Neighboor TSP
        marketRoute = self.tsp(self.cost_matrix, self.markets, 1)

        # 2OPT improvement
        marketRoute = self.simple2opt(self.cost_matrix, marketRoute)
        whereToBuy = self.whereToBuy(marketRoute, self.products, self.cost_matrix, self.offer_section)[0]

        improve = True
        objFun = self.routeCost(self.cost_matrix, marketRoute) + self.whereToBuy(marketRoute,self.products, self.cost_matrix, self.offer_section)[1]
        
        while improve:
            improve = False
            newRoute, newWhereToBuy, newFO = self.bestElimination(marketRoute, self.products, self.cost_matrix, self.offer_section)

            if newFO < objFun:
                marketRoute = newRoute
                whereToBuy = newWhereToBuy
                objFun = newFO
                improve = True

        return marketRoute, whereToBuy, objFun