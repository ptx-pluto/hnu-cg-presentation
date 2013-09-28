#!/usr/bin/env python
#============================================================================

from numpy import r_
from scipy.interpolate import interp1d, griddata
from  mpl_toolkits.mplot3d import Axes3D

import numpy as np
import matplotlib.pyplot as plt
import math

import fetcher

#============================================================================

all_list  = fetcher.get_all()
all_range = fetcher.get_range(all_list)

#============================================================================

city_positions = [[city['longitude'],city['latitude']] for city in all_list]
city_temps = [city['temp'] for city in all_list]

max_lati = math.ceil(all_range['latitude'][1])
min_lati = math.floor(all_range['latitude'][0])
max_long = math.ceil(all_range['longitude'][1])
min_long = math.floor(all_range['longitude'][0])

grid_x, grid_y = np.mgrid[min_long:max_long:200j, min_lati:max_lati:200j]

grid_z = griddata(city_positions, city_temps, (grid_x, grid_y), method='linear')

#============================================================================

def draw_map():
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_surface(grid_x, grid_y, grid_z)
    fig.show()

def draw_map_flat():
    plt.imshow(grid_z.T, extent=(min_long,max_long,min_lati,max_lati), origin='lower')
    plt.show()
    
#============================================================================

if __name__ == '__main__':
    draw_map_flat()
