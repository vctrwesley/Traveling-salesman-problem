from algoritmos import hillClimbing, geneticAlgorithm, simulatedAnnealing, tabuSearch
from utils import tspAlgorithms
import psutil
import os

process = psutil.Process(os.getpid())

# dataPath = "data/att48_d.txt"
# dataPath = "data/five_d.txt"
# dataPath = "data/p01_d.txt"
dataPath = "data/dantzig42_d.txt"	
algoritmos = [ hillClimbing, geneticAlgorithm, simulatedAnnealing, tabuSearch]

for algoritmo in algoritmos:
  result, memoryUsed, timeSpent = tspAlgorithms(algoritmo, dataPath, process)
  print(f"Algoritmo: {algoritmo.__name__}, Resultado: {result}, Memoria utilizada: {memoryUsed}KB, Tempo gasto: {timeSpent}")
