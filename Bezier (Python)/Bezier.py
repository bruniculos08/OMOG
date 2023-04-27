import random as random
from math import *
import matplotlib.pyplot as plt
import numpy as np

# Fazendo código para gerar curva de Bezier de grau 2 (3 pontos) em 3 dimensões (mas plotando em 2 por enquanto):

def quad_bezier_funcs(p0, p1, p2):
    x0, y0, z0 = p0[0], p0[1], p0[2]
    x1, y1, z1 = p1[0], p1[1], p1[2]
    x2, y2, z2 = p2[0], p2[1], p2[2]
    
    def xf(u):
        return ((1-u)**2)*x0 + 2*u*(1-u)*x1 + (u**2)*x2
    
    def yf(u):
        return ((1-u)**2)*y0 + 2*u*(1-u)*y1 + (u**2)*y2
    
    def zf(u):
        return ((1-u)**2)*z0 + 2*u*(1-u)*z1 + (u**2)*z2

    return xf, yf, zf

if __name__ == '__main__':
    p0 = [0, 0, 0]
    p1 = [1, 1, 0]
    p2 = [2, 0, 0]

    xf, yf, zf = quad_bezier_funcs(p0, p1, p2)

    extra_interval = 5
    U = np.linspace(0-extra_interval, 1+extra_interval, 1000)
    X = [xf(ui) for ui in U]
    Y = [yf(ui) for ui in U]
    Z = [zf(ui) for ui in U]

    plt.xlim(-0.5,4)
    plt.ylim(0,2)
    plt.plot(X, Y, label = "blue")
    plt.savefig("Exemplo01-Bezier.png")
    plt.show()
    plt.close()