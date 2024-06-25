from algoritmos import hillClimbing, geneticAlgorithm, simulatedAnnealing, tabuSearch
from utils import tspAlgorithms, selectDataset, loadData
import psutil
import os
import random

process = psutil.Process(os.getpid())

dataPath = selectDataset("../data")
numCities, distanceMatrix = loadData(dataPath)
initialTour = list(range(numCities))
random.shuffle(initialTour)

algoritmos = [ hillClimbing, geneticAlgorithm, simulatedAnnealing, tabuSearch]
print(f"Tour inicial: {initialTour}\n")
for algoritmo in algoritmos:
  result, memoryUsed, timeSpent = tspAlgorithms(algoritmo, dataPath, process, initialTour=initialTour)
  print(f"Algoritmo: {algoritmo.__name__}.\nMemoria utilizada: {memoryUsed}KB.\nTempo gasto: {timeSpent:.3f}s.\nCusto do tour: {result[1]:.0f}.\nTour retornado: {result[0]}.\nQuantidade de passos: {result[2]}.\n")