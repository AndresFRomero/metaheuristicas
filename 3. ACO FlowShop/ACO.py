# Ant Colony Optimization for FlowShop problem

# Libraries
import json


# Parameters
class AntColonyOptimization:

    n = 100 # Ants

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
        for j in sol[1:]:
            composeTime[machines[0],j] = composeTime[machines[0], j-1] + timeMatrix[machines[0], j-1]

        # Schedule Times
        for i in machines[1:]:
            for j in sol[1:]:
                timeA = composeTime[i-1,j] + timeMatrix[i-1,j]
                timeB = composeTime[i,j-1] + timeMatrix[i,j-1]

                composeTime[i,j] = max(timeA, timeB)
                deadTime += abs(timeA-timeB)

        # Final Makespan
        makeSpan = composeTime[machines[-1],sol[-1]] + timeMatrix[machines[-1],sol[-1]]

        return makeSpan, deadTime


    def graphCreation(self, timeMatrix: dict, jobs: set, machines: list):

        dummyCosts = {}
        for i in machines:
            for j in machines:
                if i != j:
                    dummyCosts[i,j] = self.makespan_dt([i,j], timeMatrix, machines)[1]

        return dummyCosts

    def objFun(sol:list, timeMatrix: dict):
        pass