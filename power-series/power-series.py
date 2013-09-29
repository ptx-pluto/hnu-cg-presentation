#!/usr/bin/env python
#=============================================================================================
# Generate the plot of following real functions
# sin(x), cos(x), ex, 1/(1+x), 1/(1-x)
#=============================================================================================

import numpy, math, os
from matplotlib import pyplot
from scipy import optimize, special

#=============================================================================================

DIR_NAME  = os.path.dirname(__file__)
PLOT_PATH = os.path.join(DIR_NAME, 'plots')

if not os.path.exists(PLOT_PATH):
    os.mkdir(PLOT_PATH)

#=============================================================================================

def sin_term(n):
    if n % 2 == 1:
        return lambda x: (-1)**((n-1)/2) * (x**n) / math.factorial(n)
    else: 
        return lambda x: 0

def cos_term(n):
    if n == 0:
        return lambda x: 1
    elif n % 2 == 0:
        return lambda x: (-1)**(n/2) * (x**n) / math.factorial(n)
    else: 
        return lambda x: 0

def ex_term(n):
    return lambda x: (x**n) / math.factorial(n)

#=============================================================================================

def get_series(term, depth):
    return lambda x: sum([term(n)(x) for n in range(1, depth+1)])

#=============================================================================================

def power_sin(level):
    pyplot.figure()
    pyplot.title('Power series of sin')
    interval = numpy.arange(0.0, 20.0, 0.01)
    pyplot.axis([0,20,-2,2])

    for depth in range(1,level+1,2):
        func = get_series(sin_term, depth)
        pyplot.plot(interval, func(interval), color=(1-depth/level,1-depth/level,0.2))
        pyplot.text(1, 1.5, 'iterate depth = %d' % depth)
        pyplot.savefig( PLOT_PATH + '/power-sin-'+ str(depth) + '.png', dpi=256 )

def power_cos(level):
    pyplot.figure()
    pyplot.title('Power series of cos')
    interval = numpy.arange(0.0, 20.0, 0.01)
    pyplot.axis([0,20,-2,2])

    for depth in range(2,level+1,2):
        func = get_series(cos_term, depth)
        pyplot.plot(interval, func(interval), color=(1-depth/level,1-depth/level,0.2))
        pyplot.text(1, 1.5, 'iterate depth = %d' % level)
        pyplot.savefig(os.path.join(PLOT_PATH, 'power-cos-' + str(depth) + '.png'), dpi=256 )

def power_ex():
    pyplot.figure()
    interval = numpy.arange(0.0, 20.0, 0.01)
    for depth in range(1,level+1):
        func = get_series(ex_term, depth)
        pyplot.plot(interval, func(interval), color=(1-depth/level,1-depth/level,0.2))
    pyplot.axis([0,20,-2,2])
    pyplot.title('Power series of ex')
    pyplot.text(1, 1.5, 'iterate depth = %d' % level)
    pyplot.savefig(os.path.join(PLOT_PATH, '/power-ex-' + str(level) + '.png'), dpi=256 )

#=============================================================================================

if __name__ == '__main__':
#    power_sin(70)
    power_cos(70)
