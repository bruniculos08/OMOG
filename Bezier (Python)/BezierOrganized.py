from math import *
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

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

def plot_poligon(points : list, c : str) -> None:
    plt.rcParams["figure.autolayout"] = True

    for i in range(0, len(points)-1):
        x = [points[i].x, points[i+1].x] 
        y = [points[i].y, points[i+1].y]
        plt.plot(x, y, 'bo', linestyle="--", color = c)

    plt.rcParams["figure.autolayout"] = False

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

def rotate_z_axis(points : list, angle : float) -> list:
    newPoints = deepcopy(points)
    for p in newPoints:
        new_x = p.x * cos(angle) - p.y * sin(angle)
        new_y = p.y * cos(angle) + p.x * sin(angle)
        new_z = p.z
        p.x = new_x
        p.y = new_y
        p.z = new_z
    return newPoints

def get_vector(p0 : Point, p1 : Point) -> Point:
    return Point(p1.x - p0.x, p1.y - p0.y, p1.z - p0.z)

def magnitude(vector : Point) -> float:
    return sqrt(pow(vector.x, 2) + pow(vector.y, 2) + pow(vector.z, 2))

if __name__ == '__main__':

    # Exemplo da função que calcular curvas de bezier para quaisquer número de pontos (o grau é igual ao número de pontos menos um (n-1)):
    points = [Point(0, 0, 0), Point(0.5, 1.5, 0), Point(1.25, 2, 0) , Point(2.5, 1.5, 0), 
              Point(1.5, 0.5, 0), Point(4, -1.5, 0), Point(4, 0, 0), Point(5, 1, 0)]

    plt.xlim(-5, 7)
    plt.ylim(-5, 7)

    newPoints = rotate_z_axis(deepcopy(points), pi)
    plot_poligon(newPoints, "green")
    plot_bezier(newPoints, "green")

    plot_poligon(points, "orange")
    plot_bezier(points, "orange")

    print("|v0| = ", magnitude(get_vector(points[2], points[3])))
    print("|v1| = ", magnitude(get_vector(newPoints[2], newPoints[3])))

    plt.savefig("Exemplo-Bezier.png")
    plt.show()
    plt.close()