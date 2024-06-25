import random
import math
from collections import deque

def calculateTourLength(tour, distanceMatrix):
    totalDistance = 0
    for i in range(len(tour) - 1):
        totalDistance += distanceMatrix[tour[i]][tour[i + 1]]
    totalDistance += distanceMatrix[tour[-1]][tour[0]]
    return totalDistance

def hillClimbing( numCities, distanceMatrix, initialTour=None):
    if initialTour is None:
        currentTour = list(range(numCities))
        random.shuffle(currentTour)
    else:
        currentTour = initialTour    
    
    currentLength = calculateTourLength(currentTour, distanceMatrix)
    steps = 0
    while True:
        steps += 1
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
    return currentTour, currentLength, steps

def initializePopulation(numCities, populationSize, initialTour=None):
    population = []
    if initialTour is not None:
        population.append(initialTour)
    for _ in range(populationSize):
        individual = list(range(numCities))
        random.shuffle(individual)
        population.append(individual)
    return population

def calculateDistance(path, distanceMatrix):
    totalDistance = 0
    for i in range(len(path)):
        fromCity = path[i]
        toCity = path[(i + 1) % len(path)]
        totalDistance += distanceMatrix[fromCity][toCity]
    return totalDistance

def selectForReproduction(population, fitnessScores, tournamentSize=5):
    matingPool = []
    for _ in range(len(population)):
        tournament = random.sample(list(enumerate(fitnessScores)), tournamentSize)
        winner = min(tournament, key=lambda x: x[1])
        matingPool.append(population[winner[0]])
    return matingPool

def crossover(parent1, parent2):
    cut = random.randint(1, len(parent1) - 1)
    child = parent1[:cut] + [gene for gene in parent2 if gene not in parent1[:cut]]
    return child

def mutate(individual, mutationRate):
    for i in range(len(individual)):
        if random.random() < mutationRate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
    return individual

def generateNextGeneration(matingPool, populationSize, mutationRate):
    newPopulation = []
    for _ in range(populationSize):
        parent1, parent2 = random.sample(matingPool, 2)
        child = crossover(parent1, parent2)
        child = mutate(child, mutationRate)
        newPopulation.append(child)
    return newPopulation

def geneticAlgorithm(numCities, distanceMatrix, initialTour=None):
    populationSize = 100
    maxGenerations = 1000
    mutationRate = 0.01
    elitismSize = 1 
    population = initializePopulation(numCities, populationSize, initialTour)
    bestSolution = None
    bestDistance = float('inf')
    steps = 0
    noImprovementCount = 0
    improvementThreshold = 50
    for generation in range(maxGenerations):
        steps += 1
        fitnessScores = [calculateDistance(individual, distanceMatrix) for individual in population]
        
        improved = False
        for i, score in enumerate(fitnessScores):
            if score < bestDistance:
                bestDistance = score
                bestSolution = population[i]
                improved = True

        if not improved:
            noImprovementCount += 1
        else:
            noImprovementCount = 0
        if noImprovementCount >= improvementThreshold:
            print(f"Sem melhoria significativa por {improvementThreshold} gerações.")
            break
        
        matingPool = selectForReproduction(population, fitnessScores)
        newPopulation = generateNextGeneration(matingPool, populationSize - elitismSize, mutationRate)
        newPopulation += [bestSolution] * elitismSize
        
        if generation % 100 == 0 and mutationRate < 0.05: 
            mutationRate += 0.01
        
        population = newPopulation

    return bestSolution, bestDistance, steps

def simulatedAnnealing(numCities, distanceMatrix, initialTour=None):
    if initialTour is None:
        currentTour = list(range(numCities))
        random.shuffle(currentTour)
    else:
        currentTour = initialTour    
    
    initialTemperature = 1000.0
    finalTemperature = 1.0
    alpha = 0.8 
    maxIterations = 1000

    currentLength = calculateTourLength(currentTour, distanceMatrix)
    steps = 0

    bestTour = currentTour[:]
    bestLength = currentLength

    temperature = initialTemperature

    while temperature > finalTemperature:
        steps += 1
        for _ in range(maxIterations):
            newTour = currentTour[:]
            i, j = random.sample(range(numCities), 2)
            newTour[i], newTour[j] = newTour[j], newTour[i]

            newLength = calculateTourLength(newTour, distanceMatrix)

            if newLength < currentLength or random.random() < math.exp((currentLength - newLength) / temperature):
                currentTour = newTour
                currentLength = newLength

                if currentLength < bestLength:
                    bestTour = currentTour
                    bestLength = currentLength

        temperature *= alpha

    return bestTour, bestLength, steps

def getNeighbors(tour):
    neighbors = []
    numCities = len(tour)
    for i in range(numCities):
        for j in range(i + 1, numCities):
            neighbor = tour[:]
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

def tabuSearch(numCities, distanceMatrix, initialTour=None, tabuSize=10, maxIterations=1000, patience=100):
    if initialTour is None:
        currentTour = list(range(numCities))
        random.shuffle(currentTour)
    else:
        currentTour = initialTour    
    
    currentLength = calculateTourLength(currentTour, distanceMatrix)
    steps = 0

    bestTour = currentTour[:]
    bestLength = currentLength

    tabuList = deque(maxlen=tabuSize)
    noImprovementCount = 0

    for iteration in range(maxIterations):
        steps += 1
        if noImprovementCount >= patience:
            break

        neighbors = getNeighbors(currentTour)
        neighbors = [neighbor for neighbor in neighbors if tuple(neighbor) not in tabuList]

        bestNeighbor = None
        bestNeighborLength = float('inf')

        for neighbor in neighbors:
            neighborLength = calculateTourLength(neighbor, distanceMatrix)
            if neighborLength < bestNeighborLength:
                bestNeighbor = neighbor
                bestNeighborLength = neighborLength

        if bestNeighbor and bestNeighborLength < bestLength:
            bestTour = bestNeighbor[:]
            bestLength = bestNeighborLength
            noImprovementCount = 0
        else:
            noImprovementCount += 1

        currentTour = bestNeighbor if bestNeighbor else currentTour
        currentLength = bestNeighborLength if bestNeighbor else currentLength

        tabuList.append(tuple(currentTour))

    return bestTour, bestLength, steps