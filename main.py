import numpy as np
import cv2
import random
from deap import base, creator, tools, algorithms
import matplotlib.pyplot as plt

# Load the Leonardo's drawing
image = cv2.imread('leonardo_drawing.jpg', cv2.IMREAD_GRAYSCALE)

# Define the problem: minimize the difference between the original image and the digital representation
def evaluate(individual):
    # Render the digital representation
    render = np.zeros_like(image, dtype=np.uint8)
    for shape in individual:
        cv2.fillPoly(render, [np.array(shape)], (255, 255, 255))

    # Compute the fitness as the negative difference between the rendered image and the original image
    diff = np.abs(image - render)
    fitness = -np.sum(diff)  # maximize similarity
    return fitness,

# Define genetic operators
toolbox = base.Toolbox()
toolbox.register("attr_shape", random_polygon)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_shape, n=100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", mutate_shape, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)

# Create fitness and individual classes
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Initialize population
population = toolbox.population(n=50)

# Evolutionary loop
for gen in range(100):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    population = toolbox.select(offspring, k=len(population))

# Get the best individual
best_ind = tools.selBest(population, k=1)[0]
print("Best individual:", best_ind)
print("Fitness:", best_ind.fitness.values[0])
