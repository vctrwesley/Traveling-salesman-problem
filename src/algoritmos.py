import random

def calculateTourLength(tour, distanceMatrix):
    totalDistance = 0
    for i in range(len(tour) - 1):
        totalDistance += distanceMatrix[tour[i]][tour[i + 1]]
    totalDistance += distanceMatrix[tour[-1]][tour[0]]
    return totalDistance

def hillClimbing( numCities, distanceMatrix):
    currentTour = list(range(numCities))
    random.shuffle(currentTour)
    currentLength = calculateTourLength(currentTour, distanceMatrix)
    
    while True:
        neighbors = []
        for i in range(numCities):
            for j in range(i + 1, numCities):
                neighbor = currentTour[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(neighbor)

        bestNeighbor = None
        bestLength = currentLength
        for neighbor in neighbors:
            neighbor_length = calculateTourLength(neighbor, distanceMatrix)
            if neighbor_length < bestLength:
                bestLength = neighbor_length
                bestNeighbor = neighbor

        if bestLength < currentLength:
            currentTour = bestNeighbor
            currentLength = bestLength
        else:
            break

    return currentTour, currentLength

def geneticAlgorithm(numCities, distanceMatrix):
    pass

def simulatedAnnealing(numCities, distanceMatrix):
    pass

def tabuSearch(numCities, distanceMatrix):
    pass
