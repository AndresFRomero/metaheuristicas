# Proyecto Metaheuristicas
# Andres F. Romero
# Sebastián Bueno

# Libraries
import os
import brkgaFlowShop as tpp
import time

# Lectura de Instancias
def loadData(strFile: str):
    with open(strFile, 'r') as fp:
        problem = {}
        n = 1
        for line in fp:
            line = line.rstrip('\n')
            if line == 'EOF':
                break
            elif n <= 9:
                data = line.replace(" ", "").split(':')
                try:
                    data[1] = int(data[1])
                except:
                    pass
                problem[ data[0].lower() ] = data[1]
            elif n == 10:
                pass
            elif n == 11:
                problem['products_dimension'] =  int(line)
                problem['offer_section'] = {}                   
            elif (n > problem['products_dimension']+12 and n <= problem['products_dimension']+12+problem['dimension']):
                data = line.replace("  ", " ").split()
                data = [ int(i) for i in data ]
                dataProduct = data[2:]
                problem['offer_section'][int(data[0])]  = { dataProduct[i]: dataProduct[i+1] for i in range(0,len(dataProduct),3)}
            elif n == problem['products_dimension']+13+problem['dimension']:
                problem['cost_matrix'] = {}
            elif n > problem['products_dimension']+13+problem['dimension']:
                mket = n - problem['products_dimension']-13-problem['dimension']
                costs = line.split()
                for i in range(len(costs)):
                    problem['cost_matrix'][mket,i+1] = int(costs[i])
            else:
                pass
            n += 1
    return problem

# Lista de problemas
constructive = tpp.tppConstructive()

for subdir, dirs, files in os.walk('./InstanciasLight'):
    for file in files:
        strFile = os.path.join(subdir, file)
        problem = loadData(strFile)

        start_time = time.time()

        marketRoute, whereToBuy, objFun = constructive.main(problem)

        with open('./Soluciones/Ruta_Instancia_' + file.replace("AsimSingh.","").replace("tpp", "txt"), 'w') as fp:
            for element in marketRoute:
                fp.write(str(element-1)+" ")
        fp.close()

        with open('./Soluciones/Compra_Instancia_' + file.replace("AsimSingh.","").replace("tpp", "txt"), 'w') as fp:
            for element in whereToBuy:
                fp.write(str(element-1)+" ")
        fp.close()

        print(file, objFun, round(time.time()-start_time,2) )