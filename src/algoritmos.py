import random
import math

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

def initializePopulation(numCities, populationSize):
    """
    Gera uma população inicial de soluções aleatórias.
    Cada solução é uma permutação dos índices das cidades.
    
    :param numCities: Número total de cidades no problema.
    :param populationSize: Tamanho da população a ser gerada.
    :return: Uma lista de soluções (permutações).
    """
    population = []
    for _ in range(populationSize):
        individual = list(range(numCities))
        random.shuffle(individual)
        population.append(individual)
    return population

def calculateDistance(path, distanceMatrix):
    """
    Calcula a distância total de um caminho baseado na matriz de distâncias.

    :param path: Uma lista representando a ordem das cidades visitadas.
    :param distanceMatrix: Uma matriz 2D onde o elemento [i][j] representa a distância da cidade i para a cidade j.
    :return: A distância total do caminho.
    """
    totalDistance = 0
    for i in range(len(path)):
        fromCity = path[i]
        toCity = path[(i + 1) % len(path)]
        totalDistance += distanceMatrix[fromCity][toCity]
    return totalDistance

def selectForReproduction(population, fitnessScores, tournamentSize=5):
    """
    Seleciona indivíduos para reprodução usando o método de seleção por torneio.

    :param population: A população atual de soluções.
    :param fitnessScores: Uma lista de aptidões correspondentes a cada indivíduo na população.
    :param tournamentSize: O número de indivíduos a serem selecionados para cada torneio.
    :return: Uma nova lista de indivíduos selecionados para reprodução.
    """
    matingPool = []
    for _ in range(len(population)):
        tournament = random.sample(list(enumerate(fitnessScores)), tournamentSize)
        winner = min(tournament, key=lambda x: x[1])
        matingPool.append(population[winner[0]])
    return matingPool

def crossover(parent1, parent2):
    """
    Realiza o cruzamento entre dois pais para produzir um filho.
    """
    cut = random.randint(1, len(parent1) - 1)
    child = parent1[:cut] + [gene for gene in parent2 if gene not in parent1[:cut]]
    return child

def mutate(individual, mutationRate):
    """
    Aplica uma mutação em um indivíduo com base na taxa de mutação.
    """
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

def geneticAlgorithm(numCities, distanceMatrix):
    populationSize = 100
    maxGenerations = 1000
    mutationRate = 0.01
    elitismSize = 1 
    population = initializePopulation(numCities, populationSize)
    bestSolution = None
    bestDistance = float('inf')

    for generation in range(maxGenerations):
        fitnessScores = [calculateDistance(individual, distanceMatrix) for individual in population]
        
        for i, score in enumerate(fitnessScores):
            if score < bestDistance:
                bestDistance = score
                bestSolution = population[i]
        
        matingPool = selectForReproduction(population, fitnessScores)
        newPopulation = generateNextGeneration(matingPool, populationSize - elitismSize, mutationRate)
        newPopulation += [bestSolution] * elitismSize
        
        if generation % 100 == 0 and mutationRate < 0.05: 
            mutationRate += 0.01
        
        population = newPopulation

    return bestSolution, bestDistance

def simulatedAnnealing(numCities, distanceMatrix):
    initialTemperature = 1000.0
    finalTemperature = 1.0
    alpha = 0.995 
    maxIterations = 1000

    currentTour = list(range(numCities))
    random.shuffle(currentTour)
    currentLength = calculateTourLength(currentTour, distanceMatrix)

    bestTour = currentTour[:]
    bestLength = currentLength

    temperature = initialTemperature

    while temperature > finalTemperature:
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

    return bestTour, bestLength 

def tabuSearch(numCities, distanceMatrix):
    pass
