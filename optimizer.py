#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Python code of Biogeography-Based Optimization (BBO)

Coded by: Raju Pal (emailid: raju3131.pal@gmail.com) and Himanshu Mittal (emailid: himanshu.mittal224@gmail.com)

The code template used is similar to code given at link: https://github.com/himanshuRepo/CKGSA-in-Python
 and matlab version of the BBO at link: http://embeddedlab.csuohio.edu/BBO/software/

Reference: D. Simon, Biogeography-Based Optimization, IEEE Transactions on Evolutionary Computation, in print (2008).
@author: Dan Simon (http://embeddedlab.csuohio.edu/BBO/software/)

-- Main File: Calling the Biogeography-Based Optimization(BBO) Algorithm
                for minimizing of an objective Function

Code compatible:
 -- Python: 2.* or 3.*
"""


import csv
import sys
import time

import numpy

import BBO as bbo
import benchmarks


def selector(algo, func_details, popSize, Iter):
    function_name = func_details[0]
    lb = func_details[1]
    ub = func_details[2]
    dim = func_details[3]

    if(algo==0):
        x = bbo.BBO(getattr(benchmarks, function_name), lb, ub, dim, popSize, Iter)
    return x


def main(argv):
    # Select optimizers
    BBO = True # Code by Raju Pal & Himanshu Mittal

    # Select benchmark function
    F1 = True
    F2 = False
    F3 = False
    F4 = False
    F5 = False
    F6 = False
    F7 = False
    F8 = False
    F9 = False
    F10 = False
    F11 = False
    F12 = False
    F13 = False
    F14 = False
    F15 = False
    F16 = False
    F17 = False
    F18 = False
    F19 = False

    optimizers = [BBO]
    benchmarkfuncs = [F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14, F15, F16, F17, F18, F19]

    # Select number of repetitions for each experiment.
    # To obtain meaningful statistical results, usually 30 independent runs are executed for each algorithm.
    numOfRuns = 2

    # Select general parameters for all optimizers (population size, number of iterations)
    populationSize = 30
    iterations = 500

    # Export results ?
    export = True

    # Automatically generated name by date and time
    exportToFile = "experiment" + time.strftime("%Y-%m-%d-%H-%M-%S") + ".csv"

    # Check if it works at least once
    flag = False

    # CSV Header for for the convergence
    cnvgHeader = []

    for l in range(0, iterations):
        cnvgHeader.append("Iter" + str(l + 1))

    for i, optimizer in enumerate(optimizers):
        for j, benchmarkfunc in enumerate(benchmarkfuncs):
            if((optimizer == True) and (benchmarkfunc == True)): # start experiment if an optimizer and an objective function is selected
                for _ in range(0, numOfRuns):
                    func_details = benchmarks.getFunctionDetails(j)
                    x = selector(i, func_details, populationSize, iterations)
                    if(export == True):
                        with open(exportToFile, 'a') as out:
                            writer = csv.writer(out, delimiter = ',')
                            if (flag == False): # just one time to write the header of the CSV file
                                header = numpy.concatenate([["Optimizer", "objfname", "startTime", "EndTime", "ExecutionTime"], cnvgHeader])
                                writer.writerow(header)
                            a = numpy.concatenate([[x.optimizer, x.objfname, x.startTime, x.endTime, x.executionTime], x.convergence])
                            writer.writerow(a)
                        out.close()
                    flag = True # at least one experiment

    if (flag == False): # Failed to run at least one experiment
        print("No Optomizer or Cost function is selected. Check lists of available optimizers and cost functions")


if __name__ == '__main__':
    main(sys.argv[1:])
