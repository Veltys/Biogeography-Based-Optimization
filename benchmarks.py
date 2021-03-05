# -*- coding: utf-8 -*-


"""
Python code of Biogeography-Based Optimization (BBO)

Coded by: Raju Pal (emailid: raju3131.pal@gmail.com) and Himanshu Mittal (emailid: himanshu.mittal224@gmail.com)

The code template used is similar to code given at link: https://github.com/himanshuRepo/CKGSA-in-Python
 and matlab version of the BBO at link: http://embeddedlab.csuohio.edu/BBO/software/

Reference: D. Simon, Biogeography-Based Optimization, IEEE Transactions on Evolutionary Computation, in print (2008).
@author: Dan Simon (http://embeddedlab.csuohio.edu/BBO/software/)

-- Benchmark Function File: Defining the benchmark function along its range lower bound, upper bound and dimensions

Code compatible:
 -- Python: 2.* or 3.*
"""


import ctypes
import os

import numpy

import Config


# define the function blocks
def F1(x):
    s = numpy.sum(x ** 2);
    return s


def F2(x):
    libtest = ctypes.CDLL(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'libbenchmark.' + ('dll' if os.name == 'nt' else 'so'))
    libtest.cec20_bench.argtypes = (ctypes.c_size_t, ctypes.c_size_t, ctypes.POINTER(ctypes.c_double * len(x)))
    libtest.cec20_bench.restype = ctypes.c_double

    return libtest.cec20_bench(1, x.size, (ctypes.c_double * len(x))(*x))


def getFunctionDetails(a):
    cnf = Config.Config()

    # [name, lb, ub, dim]
    param = {  0: ["F1", -100, 100, 30],
               1: ["F2", -100, 100, cnf.dimensions],
            }
    return param.get(a, "nothing")



