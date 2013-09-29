#!/usr/bin/env python
#===================================================================================================
# Scipy interpolate functionalities (2D and 3D)
#===================================================================================================

from numpy import r_
from scipy.interpolate import interp1d, griddata
from  mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt


#===================================================================================================    

func = lambda x,y: x*(1-x)*np.cos(4*np.pi*x)*np.sin(4*np.pi*y**2)**2
grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]
points = np.random.rand(1000,2)
values = func(points[:,0], points[:,1])

grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')

def interp_3d_full():
    fig = plt.figure() #figsize=plt.figaspect(0.5))

    ax = fig.add_subplot(2,2,1, projection='3d')
    ax.plot_surface(grid_x, grid_y, func(grid_x, grid_y), rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)
    ax.plot(points[:,0], points[:,1], 'k.', ms=1)
    plt.title('Original')

    ax = fig.add_subplot(2,2,2, projection='3d')
    ax.plot_surface(grid_x, grid_y, grid_z0, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)
    plt.title('Nearest')

    ax = fig.add_subplot(2,2,3, projection='3d')
    ax.plot_surface(grid_x, grid_y, grid_z1, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)
    plt.title('Linear')

    ax = fig.add_subplot(2,2,4, projection='3d')
    ax.plot_surface(grid_x, grid_y, grid_z2, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)
    plt.title('Cubic')
    
    plt.show()

def interp_3d_nearest():
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_surface(grid_x, grid_y, grid_z0, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)
    plt.show()

def interp_3d_origin():
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_surface(grid_x, grid_y, func(grid_x, grid_y), rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)
    ax.plot(points[:,0], points[:,1], 'k.', ms=1)
    plt.show()

def interp_3d_linear():
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_surface(grid_x, grid_y, grid_z1, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)
    plt.show()

def interp_3d_cubic():
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_surface(grid_x, grid_y, grid_z2, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)
    plt.show()

def interp_3d_flat():
    # original function and random points
    plt.subplot(221)
    plt.imshow(func(grid_x, grid_y).T, extent=(0,1,0,1), origin='lower')
    plt.plot(points[:,0], points[:,1], 'k.', ms=1)
    plt.title('Original')

    plt.subplot(222)
    plt.imshow(grid_z0.T, extent=(0,1,0,1), origin='lower')
    plt.title('Nearest')

    plt.subplot(223)
    plt.imshow(grid_z1.T, extent=(0,1,0,1), origin='lower')
    plt.title('Linear')

    plt.subplot(224)
    plt.imshow(grid_z2.T, extent=(0,1,0,1), origin='lower')
    plt.title('Cubic')
    
    plt.gcf().set_size_inches(6,6)
    plt.show()


#===================================================================================================

if __name__ == '__main__':
    pass
#    interp_3d_flat()
#    interp_3d_big()
#    interp_3d_origin()
#    interp_3d_full()
    
