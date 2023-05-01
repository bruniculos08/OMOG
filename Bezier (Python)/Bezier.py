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

def line_funcs(pA, pB):

    def x_line(u):
        return (pB[0]-pA[0])*u + pA[0]
    
    def y_line(u):
        return (pB[1]-pA[1])*u + pA[1]
    
    def z_line(u):
        return (pB[2]-pA[2])*u + pA[2]
    
    return x_line, y_line, z_line

def build_lerp(p0, p1):
    def lerp_x(u):
        return (1-u)*p0[0] + u*p1[0]    
    def lerp_y(u):
        return (1-u)*p0[1] + u*p1[1]
    def lerp_z(u):
        return (1-u)*p0[2] + u*p1[2] 
    return lerp_x, lerp_y, lerp_z

def lerp(p0, p1, u):
    lerp_x = (1-u)*p0[0] + u*p1[0]
    lerp_y = (1-u)*p0[1] + u*p1[1]
    lerp_z = (1-u)*p0[2] + u*p1[2]
    return [lerp_x, lerp_y, lerp_z]

def calc_bezier(points, u):
    global flag
    
    n = len(points)-1
    for i in range(n, -1, -1):
        for j in range(0, i, 1):
            point = lerp(points[j], points[j+1], u)
            points[j] = point
    
    # Ao final points conterá o ponto calculado na primeira posição (0): 
    return points[0]

def plot_poligon(points):
    plt.rcParams["figure.autolayout"] = True

    i = 0
    for i in range(0, len(points)-1):
        x = [points[i][0], points[i+1][0]] 
        y = [points[i][1], points[i+1][1]]
        plt.plot(x, y, 'bo', linestyle="--")

    plt.rcParams["figure.autolayout"] = False


# A grande beleza de uma curva de Bezier é ela terminar dentro do polígono
if __name__ == '__main__':

    # Exemplo da função que calcula apenas curvas de bezier de grau 2 (3 pontos por segmento):
    p0 = [0, 0, 0]
    p1 = [1, 1, 0]
    p2 = [2, 1, 0]

    extra_interval = 0
    U = np.linspace(0.0-extra_interval, 1+extra_interval, 1000)

    xf, yf, zf = quad_bezier_funcs(p0, p1, p2)
    X = [xf(ui) for ui in U]
    Y = [yf(ui) for ui in U]
    Z = [zf(ui) for ui in U]

    plt.xlim(-0.5,4)
    plt.ylim(0,2)

    plt.plot(X, Y, color = "orange")
    plt.savefig("Exemplo01-Bezier.png")
    #plt.show()
    plt.close()


    # Exemplo da função que calcular curvas de bezier para quaisquer número de pontos (o grau é igual ao número de pontos menos um (n-1)):
    points = [[0, 0, 0], [0.5, 1.5, 0], [1.25, 2, 0] ,[2.5, 1.5, 0], [1.5, 0.5, 0], [4, -1.5, 0], [4, 0, 0], [5, 1, 0]]
    # points = [[0, 0, 0], [0.5, 1.5, 0], [2.25, 0, 0]]
    plot_poligon(points)

    extra_interval = 0
    U = np.linspace(0.0-extra_interval, 1+extra_interval, 1000)
    P = [calc_bezier(points, ui) for ui in U]
    
    X = [point[0] for point in P]
    Y = [point[1] for point in P]
    Z = [point[2] for point in P]
    
    plt.xlim(-0.5,7)
    plt.ylim(-2,3)

    plt.plot(X, Y, color = "green")
    plt.savefig("Exemplo02-Bezier.png")
    plt.show()
    plt.close()