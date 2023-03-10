# -*- coding: utf-8 -*-
"""Untitled102.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pZOH2qN9akc4Tx6B27Nz7nKEHVKoQBbO
"""

from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as npy
import random

# timestep determines the accuracy of the euler method of integration
timestep = 0.0001
# amplitude of noise term
amp = 0.00
# the time at which the simulation ends
end_time = 100

# creates a time vector from 0 to end_time, seperated by a timestep
t = npy.arange(0,end_time,timestep)

# intialize Human (x) and Zombie (y) vectors
x = []
y = []
z=[]
# noise term to perturb differential equations
def StochasticTerm(amp):
    return (amp * random.uniform(-1,1))

"""" definition of lotka-volterra parameters"""

a = 1

b = 1

c = 1.5

d = 1
e=1
f=1
g=2

""" euler integration """

# initial conditions for the rabbit (x) and fox (y) populations at time=0
x.append(4)
y.append(2)
z.append(5)

# forward euler method of integration
# a perturbbation term is added to the differentials to make the simulation stochastic
for index in range(1,len(t)):
    
    # make parameters stochastic
#     a = a + StochasticTerm(amp)
#     b = b + StochasticTerm(amp)
#     c = c + StochasticTerm(amp)
#     d = d + StochasticTerm(amp)
    
    # evaluate the current differentials
    xd = x[index-1] * (a - b*y[index-1]-e*z[index-1])
    yd = -y[index-1]*(c - d*x[index-1])
    zd = -z[index-1]*(g - f*x[index-1])

    
    # evaluate the next value of x and y using differentials
    next_x = x[index-1] + xd * timestep
    next_y = y[index-1] + yd * timestep
    next_z = z[index-1] + zd * timestep

    # add the next value of x and y 
    x.append(next_x)
    y.append(next_y)
    z.append(next_z)

""" visualization """
    
# visualization of deterministic populations against time
plt.plot(t, x)
plt.plot(t, y)
plt.plot(t, z)
plt.xlabel('Time')
plt.ylabel('Population Size')
plt.legend(('Humans', 'Zombies','Modified Zombies'))
plt.title('Deterministic Lotka-Volterra')
plt.show()