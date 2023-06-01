import numpy as np
import random as random
import matplotlib.pyplot as plt
from copy import deepcopy
from math import *

class Point:
    x : float
    y : float
    z : float
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

"""
Funções relacionadas a curva de Bézier:
"""
def lerp(u : float, p0 : Point, p1 : Point) -> Point:
    x = u*p0.x + (1-u)*p1.x
    y = u*p0.y + (1-u)*p1.y
    z = u*p0.z + (1-u)*p1.z
    return Point(x, y, z)

def calc_bezier(u : float, points : list) -> Point:
    temp = points.copy()

    n = len(temp) - 1
    for i in range(n, -1, -1):
        for j in range(0, i):
            temp[j] = lerp(u, temp[j], temp[j+1])

    return temp[0]

def plot_bezier(points : list, c : str):

    U = np.linspace(0.0, 1, 1000)
    P = [calc_bezier(ui, points) for ui in U]

    X = [point.x for point in P]
    Y = [point.y for point in P]
    Z = [point.z for point in P]

    plt.plot(X, Y, color = c)

"""
Funções Relacionadas a curva B-Spline:
"""
def N_func(u, i, D, T):
    
    # (i) Seja a função N_i_D(u):
    N = []
    # (ii) Equivalente à:
    # for(k = 1; k <= D; k++) varia o 'd'
    for k in range(1, D+1):
        # (ii) a. Note que nos casos base, isto é, parte de baixo da árvore temos funções N_j_k onde k = 1, e note que para esta matriz...
        # ... o índice da linha é k-1 e o índice da coluna é j, assim N_j_k = N[k-1][j] (k-1 pois k começa em 1):
        line = []
        # (ii) b. para cada nível k da árvore as folhas são da forma N_j_k onde  i <= j <= i+D-k:
        # for(j = i; j <= i+D-k; j++) varia o 'i'
        for j in range(i, (i+D-k) + 1):
            if(k == 1):
                if(T[j] <= u < T[j+1]):
                    line.append(1)
                else:
                    line.append(0)
            else:
                # (ii) c. aqui ocorre quando k > 1, e portanto já há uma linha N[k] (obs.: os índices de N estarão invertidos)
                first_term = 0
                second_term = 0
                if(T[j+k-1]-T[j] != 0):
                    # (ii) d. faz-se j-i pois quando j = i tem-se j-i = 0, assim não teremos problema com os índices e não precisaremos...
                    # ... calcular as funções com 0 <= j < i apenas para preencher a linha:
                    first_term = (u - T[j])*N[k-1-1][j-i]/(T[j+k-1] - T[j])
                if(T[j+k]-T[j+1] != 0):
                    # (ii) d. faz-se j-i pois quando j = i tem-se j-i = 0, assim não teremos problema com os índices e não precisaremos...
                    # ... calcular as funções com 0 <= j < i apenas para preencher a linha:
                    second_term = (T[j+k] - u)*N[k-1-1][j+1-i]/(T[j+k] - T[j+1])
                line.append(first_term + second_term)
        # (iii) Adicionando linha (k-1)-ésima linha a matriz N:
        N.append(line)
    
    # a matriz na posição N[D-1][0] equivale a função base N_i_d (o "i" é o primeiro índice da coluna da matriz e d-1 é a linha):
    return N[D-1][0]

def calc_BSpline(points, u, D, T):
    p = Point(0, 0, 0)
    n = len(points)-1
    for i in range(0, n+1):
        p.x += points[i].x * N_func(u, i, D, T)
        p.y += points[i].y * N_func(u, i, D, T)
        p.z += points[i].z * N_func(u, i, D, T)
    return p

def getKnots(n, D):
    T = []
    for j in range(0, n+D+1):
        if(j < D):
            T.append(0)
        elif(D <= j <= n):
            T.append(j-D+1)
        else:
            T.append(n-D+2)
    return T

def plot_bspline(points, D, T):

    n = len(points)-1
    print(T)

    U = np.linspace(0.0, n-D+2, 1000)

    segments = list(set(T))
    print(segments)

    for i, segment in enumerate(segments[0:-1]):
        piece = [calc_BSpline(points, ui, D, T) for ui in U if segment <= ui <= segments[i+1]]
        X = [point.x for point in piece[0:-1]]
        Y = [point.y for point in piece[0:-1]]
        Z = [point.z for point in piece[0:-1]]

        hexadecimal = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        plt.plot(X, Y, color = hexadecimal)

"""
Funções para continuidade entre as curvas B-Spline:
"""
def plot_poligon(points : list, c : str) -> None:
    plt.rcParams["figure.autolayout"] = True

    for i in range(0, len(points)-1):
        x = [points[i].x, points[i+1].x] 
        y = [points[i].y, points[i+1].y]
        plt.plot(x, y, 'o', linestyle="--", color = c)

    plt.rcParams["figure.autolayout"] = False

def get_vector(p0 : Point, p1 : Point) -> Point:
    return Point(p1.x - p0.x, p1.y - p0.y, p1.z - p0.z)

def magnitude(vector : Point) -> float:
    return sqrt(pow(vector.x, 2) + pow(vector.y, 2) + pow(vector.z, 2))

def fix_C0(bspline_points, bezier_points):
    delta = get_vector(bezier_points[0], bspline_points[-1])
    for point in bezier_points:
        point.x += delta.x
        point.y += delta.y
        point.z += delta.z

if __name__ == "__main__":

    bspline_points = [Point(0, 0, 0), Point(0.5, 1.5, 0), Point(1.25, 2, 0),
                        Point(2.5, 1.5, 0), Point(1.5, 0.5, 0), Point(4, -1.5, 0), 
                        Point(4, 0, 0), Point(5, 1, 0), Point(4, 2, 0)]
    
    bezier_points = [Point(0, 0, 0), Point(0.5, 2, 0), Point(1.25, 2, 0) , Point(2.5, 1.5, 0), 
              Point(1.5, 0.5, 0), Point(4, -1.5, 0), Point(4, 0, 0), Point(5, 1, 0)]
    
    fix_C0(bspline_points, bezier_points)

    plot_poligon(bezier_points, "green")
    plot_bezier(bezier_points, "green")

    D = 4
    n = len(bspline_points)-1
    T = getKnots(n, D)

    plot_poligon(bspline_points, "orange")
    plot_bspline(bspline_points, D, T)

    plt.savefig("Exemplo-Join-C0-BSpline-Bezier.png")
    plt.show()
    plt.close()