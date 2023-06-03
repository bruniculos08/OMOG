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
    temp = deepcopy(points)

    n = len(temp) - 1
    for i in range(n, -1, -1):
        for j in range(0, i):
            temp[j] = lerp(u, temp[j], temp[j+1])

    return temp[0]

def Plot_Bezier(points : list, c : str):

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
        N_i_D = N_func(u, i, D, T)
        p.x += points[i].x * N_i_D
        p.y += points[i].y * N_i_D
        p.z += points[i].z * N_i_D
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

def Plot_BSpline(points, D, T):

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
Funções para continuidade entre as curvas B-Spline e plotagem de polígonos de controle:
"""
def Plot_Poligon(points : list, c : str) -> None:
    plt.rcParams["figure.autolayout"] = True

    for i in range(0, len(points)-1):
        x = [points[i].x, points[i+1].x] 
        y = [points[i].y, points[i+1].y]
        plt.plot(x, y, 'o', linestyle="--", color = c)

    plt.rcParams["figure.autolayout"] = False

def getVector(p0 : Point, p1 : Point) -> Point:
    return Point(p1.x - p0.x, p1.y - p0.y, p1.z - p0.z)

def Force_C0_BSplineToBezier(lastPoint_BSpline, Bezier_Points):
    delta = getVector(Bezier_Points[0], lastPoint_BSpline)
    for point in Bezier_Points:
        point.x += delta.x
        point.y += delta.y
        point.z += delta.z

def PointToString(P : Point) -> str:
    return '(' + str(P.x) + ',' + str(P.y) + ',' + str(P.z) + ')'

def get_MaxValues(listsOfPoints : list) -> Point:
    x_max = x_min = listsOfPoints[0][0].x
    y_max = y_min = listsOfPoints[0][0].y
    z_max = z_min = listsOfPoints[0][0].z
    for Points in listsOfPoints:
        for P in Points:
            x_max = max(x_max, P.x)
            y_max = max(y_max, P.y)
            z_max = max(z_max, P.z)
            x_min = min(x_min, P.x)
            y_min = min(y_min, P.y)
            z_min = min(z_min, P.z)
    return Point(x_max, y_max, z_max), Point(x_min, y_min, z_min)

if __name__ == "__main__":

    # Pontos de controle da curva B-Spline:
    BSpline_points = [Point(0, -1, 0), Point(0.5, 1.5, 0), Point(1.25, 2, 0),
                      Point(2.5, 1.5, 0), Point(1.5, -1, 0), Point(4, -1.5, 0), 
                      Point(4, 0, 0), Point(5, 1, 0), Point(4, 2, 0), Point(2, 4, 0)]
    
    # Parâmetros da B-Spline:
    D = 4
    n = len(BSpline_points)-1
    T = getKnots(n, D)

    # Pontos de controle da curva Bézier:
    Bezier_Points = [Point(1, 0, 0), Point(1.5, 2, 0), Point(2.25, 2, 0) , 
                     Point(2.5, 1.5, 0), Point(1.5, 0.5, 0), Point(3, -1.5, 0), 
                     Point(4, -2, 0), Point(5, -3, 0)]

    Flag = 2
    print("Digite o número de acordo com o desejado: \n 1 - Bézier seguida de BSpline \n 2 - B-Spline seguida de Bézier\n")

    # (1) Como as funções base da BSpline zeram para valores de parâmetro iguais ao último nó do vetor, para se calcular o valor...
    # ... do último ponto da BSpline deve-se fazer uma aproximação, pois matematicamente se trata de um limite, e nesse caso a...
    # ... a precisão deste cálculo será então definida pelo parâmetro h:
    h = 0.000000000001
    lastPoint_BSpline = calc_BSpline(BSpline_points, T[-1]-h, D, T)

    # (2) Esta função translada uma lista de pontos para que o primeiro destes seja igual ao passado como parâmetro:
    Force_C0_BSplineToBezier(lastPoint_BSpline, Bezier_Points)
    # Obs.: note que apesar do vetor de nós ser definido com multiplicidade nos nós incial e final para que a curva B-Spline passe...
    # ... por estes, mesmo que este não fosse o caso a função acima iria garantir continuidade C0 pois ela irá transladar a curva...
    # ... Bézier de acordo com o último ponto calculado da curva B-Spline e não de acordo com o último ponto de controle da mesma.

    # (3) Este bloco de código ajusta o limites dos eixos do gráfico para melhor visualização:
    P_max, P_min = get_MaxValues([Bezier_Points, BSpline_points])
    plt.xlim(P_min.x - 1, P_max.x + 1)
    plt.ylim(P_min.y - 1, P_max.y + 1)

    # (4) Este bloco de código plota a curva Bézier e seu polígono de controle:
    Plot_Poligon(Bezier_Points, "green")
    Plot_Bezier(Bezier_Points, "green")

    # (5) Este bloco de código plota a curva B-Spline e seu polígono de controle:
    Plot_Poligon(BSpline_points, "orange")
    Plot_BSpline(BSpline_points, D, T)

    plt.savefig("Exemplo-Join-C0-BSpline-Bezier.png")
    plt.show()
    plt.close()