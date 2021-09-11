def loadProblem(strFile):
    with open(strFile, 'r') as fp:
        problem = {}
        n = 1
        for line in fp:
            if n <= 9:
                data = line.strip().split(' : ')
                try:
                    data[1] = int(data[1])
                except:
                    pass
                problem[ data[0].lower() ] = data[1]
            
            elif n == 10:
                problem['lista_aristas_req'] = {}
            
            elif n <= problem['aristas_req']+10:
                data = line.strip().split()
                problem['lista_aristas_req'][ int(data[1].strip(',')), int(data[2].strip(')'))]  = {
                    'coste' : int(data[4]),
                    'demanda' : int(data[6])
                }
            else:
                data = line.strip().split(' : ')
                data[1] = int(data[1])
                problem[data[0].lower()] = data[1]

            n += 1
    return problem


# ================================================
# Main
# ================================================