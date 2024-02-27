#!/usr/bin/env python3
"""
Genetic algorithm implemented with Evol solving the one max problem
(maximising number of 1s in a binary string).

"""
from PIL import Image, ImageDraw
import random

from evol import Population, Evolution

SIDES = 3
POLYGON_COUNT = 100

def make_polygon():
  r = random.randrange(0,256)
  g = random.randrange(0,256)
  b = random.randrange(0,256)
  a = random.randrange(30,60)
  return(r,g,b,a)

def initialise():
  return [make_polygon() for i in range(POLYGON_COUNT)]
#SIDES was in makepoly bracket





def select(population):
  return [random.choice(population) for i in range(2)]


def combine(*parents):
  return [a if random.random() < 0.5 else b for a, b in zip(*parents)]








def evolve(population, args):
#  population.survive(fraction=0.5)
 # population.breed(parent_picker=select, combiner=combine)
  #population.mutate(mutate_function=mutate, rate=0.1)
  #return population
  draw(population.current_best.chromosome).save("solution.png")
  #draw(population.current_best.chromosome).save("solution.png")
  exit()



def draw(solution):
  image = Image.new("RGB", (200, 200))
  canvas = ImageDraw.Draw(image, "RGBA")
  for polygon in solution:
    canvas.polygon(polygon[1:], fill=polygon[0])
  return image