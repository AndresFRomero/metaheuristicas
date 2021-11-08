# Ant Colony Optimization for FlowShop problem

# Libraries
import random

# Parameters
class AntColonyOptimization:

    # ACO configuration
    ants = 5     # Ants
    iterations = 5 # Iters
    alpha = 1.5 # influence parameter
    betha = 1 # convenience parameter
    rho = 0.4    # evaporation rate

    # Parameters
    tau = {}
    nu = {}
    dummyCosts = {}
    Q = 2000
    Lks = {} # Real Route Costs

    def makespan_dt(self, sol: list, timeMatrix: dict, machines: list) -> tuple:

        deadTime = 0
        composeTime = {}

        # First Job
        for i in machines:
            if i == machines[0]:
                composeTime[i, sol[0]] = 0
            else:
                composeTime[i, sol[0]] = composeTime[i-1, sol[0]] + timeMatrix[i-1, sol[0]]

        # First Machine
        for idx, j in enumerate(sol):
            if idx == 0:
                pass
            else:
                composeTime[machines[0],j] = composeTime[machines[0], sol[idx-1]] + timeMatrix[machines[0], sol[idx-1]]

        # Schedule Times
        for i in machines[1:]:
            for idx, j in enumerate(sol):
                if idx == 0:
                    pass
                else:
                    timeA = composeTime[i-1,j] + timeMatrix[i-1,j]
                    timeB = composeTime[i,sol[idx-1]] + timeMatrix[i,sol[idx-1]]

                    composeTime[i,j] = max(timeA, timeB)
                    deadTime += abs(timeA-timeB)

        # Final Makespan
        makeSpan = composeTime[machines[-1],sol[-1]] + timeMatrix[machines[-1],sol[-1]]

        return makeSpan, deadTime


    def paramsInit(self, timeMatrix: dict, jobs: set, machines: list):

        dummyCosts = {}
        nuInit = {}
        tauInit = {}

        for i in jobs:
            dummyCosts['O',i] = 1
            nuInit['O',i] = 1
            tauInit['O',i] = 1

            for j in jobs:
                if i != j:
                    dummyCosts[i,j] = self.makespan_dt([i,j], timeMatrix, machines)[1] + 1
                    nuInit[i,j] = 1/dummyCosts[i,j]
                    tauInit[i,j] = 1

        self.nu = nuInit
        self.tau = tauInit
        self.dummyCosts = dummyCosts

    def generateSolutions(self, jobs: set):
        
        solutions=[]

        for i in range(self.ants):
            sol = ['O']
            undone = jobs.copy()
            while len(undone)>0:
                last = sol[-1]
                sol.append(random.choices(
                    population = [ i for i in undone ],
                    weights = [ (self.tau[last,i]**self.alpha)*(self.nu[last,i]**self.betha) for i in undone ],
                    k = 1
                )[0])
                undone.remove(sol[-1])
            solutions.append(sol)
        
        return solutions

    def pheromoneUpdate(self, solutions:list, timeMatrix: dict, machines:list):
    
        self.tau = { i:self.tau[i]*(1-self.rho) for i in self.tau} # Evaporation Rate

        for sol in solutions:
            searchSol = tuple(sol)
            if (searchSol in self.Lks.keys()):
                solCost = self.Lks[searchSol]['makespan']
            else:
                solCost, DT = self.makespan_dt(sol[1:], timeMatrix, machines )
                self.Lks[tuple(sol)] = { 'makespan': solCost, 'deadtime': DT }

            for idx, j in enumerate(sol):
                if j == sol[-1]:
                    pass
                else:
                    self.tau[j,sol[idx+1]] += self.Q/solCost
    
    def bestSolution(self):
        
        bestFO = float('inf')
        deadTime = float('inf')
        bestSOL = []

        for i in self.Lks:
            if self.Lks[i]['makespan'] < bestFO:
                bestFO = self.Lks[i]['makespan'] 
                deadTime = self.Lks[i]['deadtime'] 
                bestSOL = i

        return bestSOL[1:], bestFO, deadTime

    def main(self, data:dict):

        timeMatrix = data['timeMatrix']
        jobs = data['jobs']
        machines = data['machines']

        self.paramsInit(timeMatrix,jobs,machines)

        for i in range(self.iterations): #number of iterations
            solutions = self.generateSolutions(jobs)
            self.pheromoneUpdate(solutions, timeMatrix, machines)

        return self.bestSolution()