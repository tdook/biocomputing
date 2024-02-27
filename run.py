#!/usr/bin/env python3
# coding=utf-8

# Copyright (C) 2024  Paweł Widera
# ICOS, School of Computing Science, Newcastle University
#
# This program is can only be used as part of CSC2034 coursework.
# You can't redistribute it and/or share it with others.

"""
Runs the evolution for a given target image while logging the
population statistics.

Usage: run.py [options] <target-file>
       run.py -h | --help

Options:
  -s NUM, --seed=NUM    seed for a random number generator [default: 31]
  -j NUM, --jobs=NUM    number of parallel jobs [default: 1]
  -l NAME, --log=NAME   name of the log file

Evolution parameters:
  --pop-size=NUM        number of solutions in population [default: 100]
  --generations=NUM     number of evolution iterations [default: 500]

"""
import sys
import random
import pathlib

import PIL
import evol
import docopt

from evoart import evolve, initialise, draw


MAX = 255 * 200 * 200
TARGET = None


class SimpleLogger(evol.logger.BaseLogger):
    def log(self, population, **kwargs):
        values = [i.fitness for i in population]
        stats = [kwargs["generation"], min(values), max(values)]
        self.logger.info(",".join(map(str, stats)))


def evaluate(solution):
    image = draw(solution)
    diff = PIL.ImageChops.difference(image, TARGET)
    hist = diff.convert("L").histogram()
    count = sum(i * n for i, n in enumerate(hist))
    return (MAX - count) / MAX


if __name__ == "__main__":
    args = docopt.docopt(__doc__)

    # check path to the target image
    path = pathlib.Path(args["<target-file>"])
    if not path.exists():
        print("Cannot find", path, file=sys.stderr)
        exit(1)

    # load the target image and close the file
    TARGET = PIL.Image.open(path)
    TARGET.load()

    # setup logging
    if args["--log"]:
        logger = SimpleLogger(target=args["--log"])
    else:
        logger = SimpleLogger(stdout=True)

    # for reproducibility fix the RNG seed
    random.seed(int(args["--seed"]))

    # create the first population
    population = evol.Population.generate(initialise, evaluate, maximize=True,
        size=int(args["--pop-size"]), concurrent_workers=int(args["--jobs"]))

    # run the evolution
    for i in range(int(args["--generations"])):
        evolve(population, args).callback(logger.log, generation=i)

    # save best solution as image
    best = draw(population.current_best.chromosome)
    best.save(path.with_stem(path.stem + "_best"))