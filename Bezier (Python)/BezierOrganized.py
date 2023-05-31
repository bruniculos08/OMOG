from math import *
import numpy as np
import matplotlib.pyplot as plt

class Point:
    x : float
    y : float
    z : float
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def lerp(u : float, p0 : Point, p1 : Point) -> Point:
    x = u*p0.x + (1-u)*p1.x
    y = u*p0.y + (1-u)*p1.y
    z = u*p0.z + (1-u)*p1.z
    return Point(x, y, z)

def plot_poligon(points : list):
    plt.rcParams["figure.autolayout"] = True

    for i in range(0, len(points)-1):
        x = [points[i].x, points[i+1].x] 
        y = [points[i].y, points[i+1].y]
        plt.plot(x, y, 'bo', linestyle="--")

    plt.rcParams["figure.autolayout"] = False

def calc_bezier(u : float, points : list) -> Point:
    temp = points.copy()

    n = len(temp) - 1
    for i in range(n, -1, -1):
        for j in range(0, i):
            temp[j] = lerp(u, temp[j], temp[j+1])

    return temp[0]

def plot_bezier(points : list):

    U = np.linspace(0.0, 1, 1000)
    P = [calc_bezier(ui, points) for ui in U]

    X = [point.x for point in P]
    Y = [point.y for point in P]
    Z = [point.z for point in P]

    plt.plot(X, Y, color = "blue")

def rotate_z_axis(points : list, angle : float):
    newPoints = points.copy()
    for p in newPoints:
        p.x = p.x


if __name__ == '__main__':

    # Exemplo da função que calcular curvas de bezier para quaisquer número de pontos (o grau é igual ao número de pontos menos um (n-1)):
    points = [Point(0, 0, 0), Point(0.5, 1.5, 0), Point(1.25, 2, 0) , Point(2.5, 1.5, 0), 
              Point(1.5, 0.5, 0), Point(4, -1.5, 0), Point(4, 0, 0), Point(5, 1, 0)]

    plot_poligon(points)
    plot_bezier(points)
    
    plt.savefig("Exemplo-Bezier.png")
    plt.show()
    plt.close()