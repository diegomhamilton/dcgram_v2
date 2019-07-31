# This code simulates the duffing oscillator:
# Damped driven harmonic oscillator in a double well potential.
# F = -beta*dx/dt + 2*a*x - 4*b*x^3 + A*cos(omega*t)
# Second order nonlinear differential equation numerically solved by Taylor expansion.

# For the current set of parameters the motion is chaotic, i.e.
# the motion is strongly sensitive to the initial conditions. Additionally
# no fixed period of motion is observed. The poincare plot is a fractal.

import sys
sys.path.insert(0, '..')
import numpy as np
import matplotlib.pyplot as plt
import time
from math import ceil
import bisect
import yaml

def x_2(x,v,beta,a,b):
    '''
    second derivative term for Taylor series
    '''
    return -beta*v + 2.0*a*x - 4.0*b*x*x*x

def x_3(x2,x,v,beta,a,b):
    '''
    third derivative term for Taylor series
    '''
    return -beta*x2 + 2.0*a*v -12.0*b*x*x*v

def x_4(x3,x2,x,v,beta,a,b):
    '''
    fourth derivative term for Taylor series
    '''
    return -beta*x3 + 2.0*a*x2 -12.0*b*x*x*x2 - 24.0*b*v*v*x

def x_5(x4,x3,x2,x,v,beta,a,b):
    '''
    fifth derivative term for Taylor series
    '''
    return -beta*x4 + 2*a*x3 -12.0*b*(x*x*x3 + 2.0*x2*x*v) -24.0*b*(v*v*v+2*x*v*x2)

def solve_equation(a = 0.5, b = 1/16.0, A = 2.5, omega = 2.0, beta = 0.1, N = 32, L = 1000000):
    period = 2*np.pi/(1.0*omega)
    h = period/N # time step
    # length of the simulation
    # T = 100000
    # t = np.linspace(0, 100000*period, 5500000)
    # h = 100000*period/5500000
    t = np.arange(0, L*period, h)
    # t = np.arange(0,T,h)

    t1 = time.time() #times the computation

    # Trigonometric terms in derivatives. Evaluate before the loop
    x2F = A*np.cos(omega*t)
    x3F = -A*omega*np.sin(omega*t)
    x4F = -A*omega*omega*np.cos(omega*t)
    x5F = A*omega*omega*omega*np.sin(omega*t)

    # coefficients in front of Taylor series expansion
    # Evaluate before the loop
    coef1 = 0.5*h**2.0
    coef2 = 1.0/6.0*h**3.0
    coef3 = 1.0/24.0*h**4.0
    coef4 = 1.0/120.0*h**5.0

    # initial conditions
    v = 0.0
    x = 0.5

    position = np.zeros(len(t))
    velocity = np.zeros(len(t))
    position[0] = x

    for i in range(1,len(t)):
        d2 = x_2(x,v,beta,a,b) + x2F[i]
        d3 = x_3(d2,x,v,beta,a,b) + x3F[i]
        d4 = x_4(d3,d2,x,v,beta,a,b) + x4F[i]
        d5 = x_5(d4,d3,d2,x,v,beta,a,b) + x5F[i]
        # Taylor series expansion for x,v. Order h^5
        x += v*h + coef1*d2 + coef2*d3 + coef3*d4 + coef4*d5
        v += d2*h + coef1*d3 + coef2*d4 + coef3*d5
        position[i] = x
        velocity[i] = v

    ##f = open('data_duffing_pos_vel.txt','w')
    ##for i in range(len(t)):
    ##    f.write('%f %f' %(position[i], velocity[i]))
    ##f.close()

    # # obtain phase space points at integer multiples of the period for Poincare plot
    # strange_attractor = np.zeros([len(t),2])
    # # strange_attractor = np.zeros([int(T/period),2])
    # k = 1
    # for i in range(len(t)):
    #     if abs(t[i]-k*period)<h:
    #         strange_attractor[k-1,0] = position[i]
    #         strange_attractor[k-1,1] = velocity[i]
    # #         print(k)
    #         k+=1

    t2 = time.time()
    print('computation takes ' + str(t2-t1) + ' seconds.')

    # plt.plot(t,position,'g-',linewidth=4.0)
    # # plt.axis([0, 100, -2, 2])
    # plt.title('Trajectory of the oscillator',{'fontsize':24})
    # plt.xlabel('time',{'fontsize':24})
    # plt.ylabel('Position',{'fontsize':24})
    # plt.tick_params(axis='both',labelsize=24)
    # plt.axis([0, 1000, -4, 4])
    # plt.show()

    return position

def quantize(data, N = 4):
    x = data.copy()
    x.sort()
    # Generate intervals of quantization based on entropy rate
    interval = []
    interval.append(x[0])
    for i in range(2, N+1):
        interval.append(x[ceil((i-1)*len(x)/N)])
    interval.append(x[-1])
    quantized = []
    # Quantize all symbols in data
    for symbol in data:
        new = bisect.bisect_right(interval[:-1], symbol) - 1
        quantized.append(new)    # corrects index in 0
    # Converts quantized data to string
    seq = ''.join(str(i) for i in quantized)
    
    return seq

def generate_time_series(beta = 0.1, step = 23, N = 4, version = 'v1', L = 1000000):
    data_raw = solve_equation(beta = beta, L = L)
    data = data_raw[::23]
    seq = quantize(data, N=N)

    with open(f'../dcgram_files/duffing_equation_{version}/original/original_len_{len(seq)}.yaml', 'w') as f:
        yaml.dump(seq, f)
