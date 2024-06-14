from algoritmos import hillClimbing, geneticAlgorithm, simulatedAnnealing, tabuSearch
from time import time

def tspAlgorithms(algorithm, dataPath, process):
    numCities, distanceMatrix = loadData(dataPath) 
    args = (numCities, distanceMatrix)
    memoryUsed = process.memory_info().rss / 1024.0
    start = time()
    result = algorithm(*args)
    end = time()
    timeSpent = end - start
    memoryUsed = process.memory_info().rss / 1024.0 - memoryUsed
    return result, memoryUsed, timeSpent
    
    
def loadData(filename):
    with open(filename, "r") as file:
        distanceMatrix = []
        for line in file:
            distances = line.strip().split()
            distances = [float(distance) for distance in distances]
            distanceMatrix.append(distances)
        numCities = len(distanceMatrix)
    return numCities, distanceMatrix