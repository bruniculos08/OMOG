import random as random
from math import *
import matplotlib.pyplot as plt
import numpy as np

# Estou a partir deste código usando como referência as seguintes notas de aula:
# https://web.cse.ohio-state.edu/~dey.8/course/784/

def N_func(u, i, D, T):
    
    if(D == 1):
        if(T[i] <= u < T[i+1]):
            return 1
        else:
            return 0

    first_term = 0
    second_term = 0

    #Obs.: para 

    if(T[i+D-1] - T[i] != 0):
        first_term = (u - T[i])*N_func(u, i, D-1, T)/(T[i+D-1] - T[i])

    if(T[i+D]- T[i+1] != 0):
        second_term = (T[i+D] - u)*N_func(u, i+1, D-1, T)/(T[i+D]- T[i+1])

    return first_term + second_term
    
def calc_BSpline(points, u, D, T):
    p = [0, 0, 0]
    n = len(points)-1
    for i in range(0, n+1):
        p[0] += points[i][0] * N_func(u, i, D, T)
        p[1] += points[i][1] * N_func(u, i, D, T)
        p[2] += points[i][2] * N_func(u, i, D, T)
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

def plot_poligon(points):
    plt.rcParams["figure.autolayout"] = True

    i = 0
    for i in range(0, len(points)-1):
        x = [points[i][0], points[i+1][0]] 
        y = [points[i][1], points[i+1][1]]
        plt.plot(x, y, 'bo', linestyle="--")

    plt.rcParams["figure.autolayout"] = False

if __name__ == "__main__":
    print("Hello World!")

    points = [[0, 0, 0], [0.5, 1.5, 0], [1.25, 2, 0] ,[2.5, 1.5, 0], [1.5, 0.5, 0], [4, -1.5, 0], [4, 0, 0], [5, 1, 0]]

    # (i) O número de pontos é n+1
    n = len(points)-1
    # (ii) D define o grau da curva BSpline que terá então grau D-1:
    D = 3
    # Obs. 1: a curva será C_k-2 , isto é, continua até (k-2)-ésima derivada; 
    # Obs. 2: se D = n+1 teremos uma Bézier com n+1 pontos de controle; 

    # (iii) O algoritmo que estamos utilizando para o número de nós força que a curva passe...
    # ... pelo primeiro e último ponto:
    T = getKnots(n, D)
    print(T)

    # (iv) Plotando o polígono de controle:
    plot_poligon(points)

    U = np.linspace(0.0, n-D+2, 1000)
    P = [calc_BSpline(points, ui, D, T) for ui in U]

    # Obs.: se deixarmos o último valor de u para ser calculado o plot irá ligar o último ponto...
    # ... ao ponto inicial:
    X = [point[0] for point in P[0:-2]]
    Y = [point[1] for point in P[0:-2]]
    Z = [point[2] for point in P[0:-2]]

    plt.xlim(-0.5,7)
    plt.ylim(-2,3)

    # size = len(X)

    # for i in enumerate(segments):
    #     hexadecimal = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
    #     magical_number = int(len(X)/pieces)
    #     plt.plot(X[magical_number*i:magical_number* i+1], Y[magical_number*i:magical_number* i+1], color = hexadecimal)

    plt.plot(X, Y, color = "green")
    plt.savefig("Exemplo01-BSpline.png")
    plt.show()
    plt.close()