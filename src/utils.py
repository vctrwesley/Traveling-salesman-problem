from time import time
import os

def tspAlgorithms(algorithm, dataPath, process, initialTour=None):
    numCities, distanceMatrix = loadData(dataPath) 
    args = (numCities, distanceMatrix, initialTour)
    memoryUsed = process.memory_info().rss / 1024.0
    start = time()
    result = algorithm(*args)
    end = time()
    timeSpent = end - start
    memoryUsed = process.memory_info().rss / 1024.0 - memoryUsed
    return result, memoryUsed, timeSpent

def selectDataset(dataPath):
    files = os.listdir(dataPath)
    print("Available datasets:")
    for i, file in enumerate(files):
        file = file.split(".")[0]
        print(f"{i+1}. {file}")
    while True:
        try:
            choice = int(input("Select a dataset: "))
            if choice < 1 or choice > len(files):
                raise ValueError
            break
        except ValueError:
            print("Invalid choice. Please try again.")
    selectedFile = files[choice-1]
    return os.path.join(dataPath, selectedFile)

def loadData(filename):
    with open(filename, "r") as file:
        distanceMatrix = []
        for line in file:
            distances = line.strip().split()
            distances = [float(distance) for distance in distances]
            distanceMatrix.append(distances)
        numCities = len(distanceMatrix)
    return numCities, distanceMatrix