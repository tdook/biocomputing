#!/usr/bin/env python3
"""
Genetic algorithm implemented with Evol solving the one max problem
(maximising number of 1s in a binary string).

"""
from PIL import Image, ImageDraw
import random

from evol import Population, Evolution


def initialise():
  return [random.choice([0, 1]) for i in range(16)]


def evaluate(x):
  return sum(x)


def select(population):
  return [random.choice(population) for i in range(2)]


def combine(*parents):
  return [a if random.random() < 0.5 else b for a, b in zip(*parents)]


def flip(x, rate):
  return [1 ^ i if random.random() < rate else i for i in x]


population = Population.generate(initialise, evaluate, size=10, maximize=True)
population.evaluate()




def evolve(population, args):
  population.survive(fraction=0.5)
  population.breed(parent_picker=select, combiner=combine)
  population.mutate(mutate_function=mutate, rate=0.1)
  return population

def draw(solution):
  image = Image.new("RGB", (200, 200))
  canvas = ImageDraw.Draw(image, "RGBA")
  for polygon in solution:
    canvas.polygon(polygon[1:], fill=polygon[0])
  return image