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

def calc_Bezier(u : float, points : list) -> Point:
    temp = deepcopy(points)

    n = len(temp) - 1
    for i in range(n, -1, -1):
        for j in range(0, i):
            temp[j] = lerp(u, temp[j], temp[j+1])

    return temp[0]

def dk_B_func(u, i, n, k):
    if((i > n or i < 0) and k == 0):
        return 0

    if(k == 0):
        return factorial(n)/(factorial(i)*factorial(n-i)) * pow(u, i) * pow(1-u, n-i)

    first_term = dk_B_func(u, i-1, n-1, k-1)
    second_term = dk_B_func(u, i, n-1, k-1)

    return n*(first_term - second_term)

def calc_derivative_Bezier(u, Bezier_Points, k):
    P = Point(0, 0, 0)
    n = len(Bezier_Points)-1
    for i in range(0, n+1):
        dk_B = dk_B_func(u, i, n, k)
        P.x += Bezier_Points[i].x * dk_B
        P.y += Bezier_Points[i].y * dk_B
        P.z += Bezier_Points[i].z * dk_B
    return P

def Bezier_EndPoint_SecondDerivative(Bezier_Points):
    n = len(Bezier_Points)-1
    x = n*(n-1)*(Bezier_Points[2].x - 2*Bezier_Points[1].x + Bezier_Points[0].x)
    y = n*(n-1)*(Bezier_Points[2].y - 2*Bezier_Points[1].y + Bezier_Points[0].y)
    z = n*(n-1)*(Bezier_Points[2].z - 2*Bezier_Points[1].z + Bezier_Points[0].z)
    dB = Point(x, y, z)
    return dB

def Plot_Bezier(points : list, c : str):

    U = np.linspace(0.0, 1, 1000)
    P = [calc_Bezier(ui, points) for ui in U]

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

def calc_Bspline(points, u, D, T):
    p = Point(0, 0, 0)
    n = len(points)-1
    for i in range(0, n+1):
        N_i_D = N_func(u, i, D, T)
        p.x += points[i].x * N_i_D
        p.y += points[i].y * N_i_D
        p.z += points[i].z * N_i_D
    return p

def dk_N_func(u, i, D, T, k):

    first_term = 0
    second_term = 0

    if(T[i+D-1] - T[i] != 0):
        first_term = (D-1)/(T[i+D-1] - T[i])

    if(T[i+D] - T[i+1] != 0):
        second_term = (D-1)/(T[i+D] - T[i+1])

    if(k == 0):
        result = N_func(u, i, D, T)
    else:
        result = first_term * dk_N_func(u, i, D-1, T, k-1) - second_term * dk_N_func(u, i+1, D-1, T, k-1)
    return result

def calc_derivative_Bspline(points, u, D, T, k):
    p = Point(0, 0, 0)
    n = len(points)-1
    for i in range(0, n+1):
        dN_i_D = dk_N_func(u, i, D, T, k)
        p.x += points[i].x * dN_i_D
        p.y += points[i].y * dN_i_D
        p.z += points[i].z * dN_i_D
    return p

def Bspline_EndPoint_Derivative(Bspline_points, D, T):
    n = len(Bspline_points)-1
    Q = getVector(Bspline_points[n-1], Bspline_points[n])
    term = (D-1)/(T[n+D-1] - T[n])
    return Point(Q.x * term, Q.y * term, Q.z * term)

def getKnots(n, D):
    # Caso se queira alterar o vetor de nós pode-se alterar esta parte do código:
    T = []
    for j in range(0, n+D+1):
        if(j < D):
            T.append(0)
        elif(D <= j <= n):
            T.append(j-D+1)
        else:
            T.append(n-D+2)
        # T.append(j/(n+D))
        # T.append(j**5)
    return T

def Plot_Bspline(points, D, T):

    n = len(points)-1
    print("Vetor de nós (B-spline): " + str(T))

    # A curva B-spline é definida apenas no intervalo em que T[D-1] <= u < T[n+1], pois este é o intervalo em que...
    # ... a soma das funções base é igual à 1 (isso pode ser provado por indução):
    U = np.linspace(T[D-1], T[n+1], 1000)

    # Os intervalos entre vetores de nós são os locais da reta real onde diferentes funções base são diferentes de zero:
    for i in range(D-1, n+1):
        piece = [calc_Bspline(points, ui, D, T) for ui in U if T[i] <= ui < T[i+1]]
        X = [point.x for point in piece]
        Y = [point.y for point in piece]
        Z = [point.z for point in piece]

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

def Force_C0_BsplineToBezier(lastPoint_Bspline, Bezier_Points) -> None:
    delta = getVector(Bezier_Points[0], lastPoint_Bspline)
    for point in Bezier_Points:
        point.x += delta.x
        point.y += delta.y
        point.z += delta.z

def Force_C1_BsplineToBezier(Bspline_Points, Bezier_Points, D, T, h):
    # dS = Bspline_EndPoint_Derivative(Bspline_Points, D, T)
    dS = calc_derivative_Bspline(Bspline_Points, T[n+1]-h, D, T, 1)
    print("S'(" + str(T[-1]) + ") = " + PointToString(dS))

    m = len(Bezier_Points) - 1
    B0 = Bezier_Points[0]
    B1 = Point(dS.x/m + B0.x, dS.y/m + B0.y, dS.z/m + B0.z)
    Bezier_Points[1] = B1

    dB = calc_derivative_Bezier(0, Bezier_Points, 1)
    print("B'(" + str(0) + ") = " + PointToString(dB) + "\n")


def Force_C2_BsplineToBezier(Bspline_Points, Bezier_Points, D, T, h):
    second_dS = calc_derivative_Bspline(Bspline_Points, T[n+1]-h, D, T, 2)
    print("S''(" + str(T[-1]) + ") = " + PointToString(second_dS))
    
    m = len(Bezier_Points)-1
    B0 = Bezier_Points[0]
    B1 = Bezier_Points[1]
    B2 = Point(second_dS.x/(m*(m-1))+2*B1.x-B0.x, 
               second_dS.y/(m*(m-1))+2*B1.y-B0.y, 
               second_dS.z/(m*(m-1))+2*B1.z-B0.z)

    Bezier_Points[2] = B2

    second_dB = calc_derivative_Bezier(0, Bezier_Points, 2)
    print("B''(" + str(0) + ") = " + PointToString(second_dB) + "\n")

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
    Bspline_Points = [Point(0, 1, 0), Point(1, 1.5, 0), Point(2, 2, 0),
                        Point(3, 1.5, 0), Point(4, 0.5, 0), Point(5, -1.5, 0), 
                        Point(6, 0, 0), Point(7, 4, 0), Point(7.5, 3.8, 0)]
    
    # Parâmetros da B-Spline:
    D = 4
    n = len(Bspline_Points)-1
    T = getKnots(n, D)

    # Pontos de controle da curva Bézier:
    Bezier_Points = [Point(1, -1, 0), Point(2, 2, 0), Point(1.25, 3, 0) , Point(2.5, 3.5, 0), 
                    Point(1.5, 5.5, 0), Point(4, -0.5, 0), Point(4, 0, 0), Point(5, 2, 0)]

    # (1) Como as funções base da Bspline zeram para valores de parâmetro iguais ao último nó do vetor, para se calcular o valor...
    # ... do último ponto da Bspline deve-se fazer uma aproximação, pois matematicamente se trata de um limite, e nesse caso a...
    # ... a precisão deste cálculo será então definida pelo parâmetro h:
    h = 0.00000000000001
    lastPoint_Bspline = calc_Bspline(Bspline_Points, T[n+1]-h, D, T)

    # (2) Esta função translada uma lista de pontos para que o primeiro destes seja igual ao passado como parâmetro:
    Force_C0_BsplineToBezier(lastPoint_Bspline, Bezier_Points)
    # Obs.: note que apesar do vetor de nós ser definido com multiplicidade nos nós incial e final para que a curva B-Spline passe...
    # ... por estes, mesmo que este não fosse o caso a função acima iria garantir continuidade C0 pois ela irá transladar a curva...
    # ... Bézier de acordo com o último ponto calculado da curva B-Spline e não de acordo com o último ponto de controle da mesma.

    # (3) Esta função calcula um novo ponto de controle P1 para a curva Bézier para que se force continuidade C1:
    Force_C1_BsplineToBezier(Bspline_Points, Bezier_Points, D, T, h)
    # Obs.: assim como para o cálculo da curva B-spline no último parâmetro do vetor de nós é necessário um valor h que definirá...
    # ... a precisão do cálculo da derivada da B-spline neste ponto.

    # (4) Esta função calcula um novo ponto de controle P2 para a curva Bézier para que se force continuidade C2:
    Force_C2_BsplineToBezier(Bspline_Points, Bezier_Points, D, T, h)
    # Obs.: assim como para o cálculo da curva B-spline no último parâmetro do vetor de nós é necessário um valor h que definirá...
    # ... a precisão do cálculo da segunda derivada da B-spline neste ponto.

    # (4) Este bloco de código ajusta o limites dos eixos do gráfico para melhor visualização:
    P_max, P_min = get_MaxValues([Bezier_Points, Bspline_Points])
    plt.xlim(P_min.x - 1, P_max.x + 1)
    plt.ylim(P_min.y - 1, P_max.y + 1)

    # (5) Este bloco de código plota o polígono de controle de cada uma das curvas:
    Plot_Poligon(Bezier_Points, "blue")
    Plot_Poligon(Bspline_Points, "orange")
    
    # (4) Este bloco de código plota a curva Bézier e a curva B-spline:
    Plot_Bezier(Bezier_Points, "green")
    Plot_Bspline(Bspline_Points, D, T)

    plt.savefig("Exemplo-Join-C2-Bspline-Bezier.png")
    plt.show()
    plt.close()