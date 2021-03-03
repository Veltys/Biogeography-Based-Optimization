# -*- coding: utf-8 -*-


"""
Python code of Biogeography-Based Optimization (BBO)

Coded by: Raju Pal (emailid: raju3131.pal@gmail.com) and Himanshu Mittal (emailid: himanshu.mittal224@gmail.com)

The code template used is similar to code given at link: https://github.com/himanshuRepo/CKGSA-in-Python
 and matlab version of the BBO at link: http://embeddedlab.csuohio.edu/BBO/software/

Reference: D. Simon, Biogeography-Based Optimization, IEEE Transactions on Evolutionary Computation, in print (2008).
@author: Dan Simon (http://embeddedlab.csuohio.edu/BBO/software/)

-- BBO File: Performing the Biogeography-Based Optimization(BBO) Algorithm

Code compatible:
 -- Python: 2.* or 3.*
"""


from __future__ import division

import random
import time

import numpy

import ClearDups
from solution import solution


def BBO(objf, lb, ub, dim, popSize, iters):
    # Defining the solution variable for saving output variables
    s = solution()

    # Initializing BBO parameters
    pmutate = 0.01; # initial mutation probability
    keep = 2; # elitism parameter: how many of the best habitats to keep from one generation to the next

    # Initializing the parameters with default values
    fit = numpy.zeros(popSize)
    eliteSolution = numpy.zeros((keep, dim))
    eliteCost = numpy.zeros(keep)
    island = numpy.zeros((popSize, dim))
    mu = numpy.zeros(popSize)
    lambda1 = numpy.zeros(popSize)
    minCost = numpy.zeros(iters)
    # Bestpos = numpy.zeros(dim)

    # Initializing Population
    pos = numpy.random.uniform(0, 1, (popSize, dim)) * (ub - lb) + lb

    #Calculate objective function for each particle
    for i in range(popSize):
        # Performing the bound checking
        pos[i,:] = numpy.clip(pos[i,:], lb, ub)
        fitness = objf(pos[i,:])
        fit[i] = fitness

    # Calculating the mu and lambda
    for i in range(popSize):
        mu[i] = (popSize + 1 - (i)) / (popSize + 1)
        lambda1[i] = 1 - mu[i]

    print("BBO is optimizing  \"" + objf.__name__ + "\"")

    timerStart = time.time()
    s.startTime = time.strftime("%Y-%m-%d-%H-%M-%S")

    # Defining the loop
    for l in range(iters):
        # Defining the Elite Solutions
        for j in range(keep):
            eliteSolution[j,:] = pos[j,:]
            eliteCost[j] = fit[j]

        # Performing Migration operator
        for k in range(popSize):
            for j in range(dim):
                if random.random() < lambda1[k]:
                    # Performing Roulette Wheel
                    randomNum = random.random() * sum(mu)
                    select = mu[1]
                    selectIndex = 0
                    while (randomNum > select) and (selectIndex < (popSize-1)):
                        selectIndex = selectIndex + 1;
                        select = select + mu[selectIndex];

                    island[k, j] = pos[selectIndex, j]
                else:
                    island[k, j] = pos[k, j]

        # Performing Mutation
        for k in range(popSize):
            for parnum in range(dim):
                if pmutate > random.random():
                    island[k, parnum] = lb + (ub - lb) * random.random();

        # Performing the bound checking
        for i in range(popSize):
            island[i,:] = numpy.clip(island[i,:], lb, ub)

        # Replace the habitats with their new versions.
        for k in range(popSize):
            pos[k,:] = island[k,:]

        #Calculate objective function for each individual
        for i in range(popSize):
            fitness = objf(pos[i,:])
            fit[i] = fitness

        # Sort the fitness
        # fitnessSorted = numpy.sort(fit)

        # Sort the population on fitness
        ii = numpy.argsort(fit)
        pos = pos[ii,:]

        # Replacing the individual of population with eliteSolution
        for k in range(keep):
            pos[(popSize - 1) - k,:] = eliteSolution[k,:];
            fit[(popSize - 1)] = eliteCost[k];

        # Removing the duplicate individuals
        pos = ClearDups.ClearDups(pos, popSize, dim, ub, lb)

        #Calculate objective function for each individual
        for i in range(popSize):
            fitness = objf(pos[i,:])
            fit[i] = fitness

        # Sort the fitness
        # fitnessSorted = numpy.sort(fit)

        # Sort the population on fitness
        ii = numpy.argsort(fit)
        pos = pos[ii,:]

        # Saving the best individual
        minCost[l] = fit[1]
        # Bestpos = pos[1,:]
        gBestScore = fit[1]

        # Displaying the best fitness of each iteration
        if (l % 1 == 0):
            print(['At iteration ' + str(l + 1) + ' the best fitness is ' + str(gBestScore)])

    timerEnd = time.time()
    s.endTime = time.strftime("%Y-%m-%d-%H-%M-%S")
    s.executionTime = timerEnd - timerStart
    s.convergence = minCost
    s.optimizer = "BBO"
    s.objfname = objf.__name__

    return s
