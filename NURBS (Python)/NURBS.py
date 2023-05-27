import random as random
from math import *
import matplotlib.pyplot as plt
import numpy as np

# Estou a partir deste código usando como referência as seguintes notas de aula:
# https://web.cse.ohio-state.edu/~dey.8/course/784/

# Obs.: este código cálcula a B-Spline de maneira dinâmica (método mais eficiente) montando...
# ... a árvore de cada função N_i_D(u) de baixo para cima sem recalcular o itens já calculados...
# ... de modo que a complexidade é de O(D²)

def N_func(u, i, D, T):

    global counter
    counter += 1

    if(D == 1):
        if(T[i] <= u < T[i+1]):
            return 1
        else:
            return 0

    first_term = 0
    second_term = 0

    # Obs.: em certas situações pode ocorrer divisão por 0 e nestes casos devemos colocar o valor resultante...
    # ... como 0, por isso os termos são inicializados como iguais à 0 e cada um só é calculado caso o denominador...
    # ... do termo seja diferente de 0;

    if(T[i+D-1] - T[i] != 0):
        first_term = (u - T[i])*N_func(u, i, D-1, T)/(T[i+D-1] - T[i])

    if(T[i+D]- T[i+1] != 0):
        second_term = (T[i+D] - u)*N_func(u, i+1, D-1, T)/(T[i+D]- T[i+1])

    return first_term + second_term

def R_func(u, i, D, T, n, weights):
    
    numerator = weights[i]*N_func(u, i, D, T)
    denominator = calc_SUM(n, u, D, T, weights)
    
    return numerator/denominator


def calc_SUM(n, u, D, T, weights):
    sum = 0
    for j in range(0, n+1):
        sum += weights[j] * N_func(u, j, D, T)
    return sum

def calc_NURBS(points, u, D, T, weights):
    p = [0, 0, 0]
    n = len(points)-1
    for i in range(0, n+1):
        p[0] += points[i][0] * R_func(u, i, D, T, n, weights)
        p[1] += points[i][1] * R_func(u, i, D, T, n, weights)
        p[2] += points[i][2] * R_func(u, i, D, T, n, weights)
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

    global counter
    counter = 0

    points = [[0, 0, 0], [0.5, 1.5, 0], [1.25, 2, 0] ,
              [2.5, 1.5, 0], [1.5, 0.5, 0], [4, -1.5, 0], 
              [4, 0, 0], [5, 1, 0], [6, 3, 0]]

    weights = [1 for point in points]
    weights[3] = 0.1
    weights[4] = 2

    # (i) O número de pontos é n+1
    n = len(points)-1
    # (ii) D define o grau da curva BSpline que terá então grau D-1:
    D = 4
    # Obs. 1: a curva será C_k-2 , isto é, continua até (k-2)-ésima derivada; 
    # Obs. 2: se D = n+1 teremos uma Bézier com n+1 pontos de controle; 
    # Obs. 2: D deve estar no intervalo [2, n]; 

    # (iii) O algoritmo que estamos utilizando para o número de nós força que a curva passe...
    # ... pelo primeiro e último ponto:
    T = getKnots(n, D)
    print(T)
    # Obs. 1: este vetor de nós é não uniforme e o primeiro e o último nós tem multiplicidade igual a D para que...
    # ... a curva passe por P_0 e P_n;

    # (iv) Plotando o polígono de controle:
    plot_poligon(points)

    U = np.linspace(0.0, n-D+2, 1000)
    # P = [calc_BSpline(points, ui, D, T) for ui in U]

    # (v) os segmentos são formados pelos intervalos de tamanho maior que 0 no vetor de nós pois estes são os intervalos...
    # ... em que diferentes pontos de controle tem influência visto que em um determinado intervalo [T[i], T[i+1]] determinadas funções...
    # ... funções estarão todas zeradas, mais espercificamente, as únicas funções que não estarão zeradas são as da forma N_j,_D(u) tal...
    # ... que i - D + 1 =< j <= i se u E [T[i], T[i+1]] pois note que:
    #       
    #       a. se j = i - D + 1 então as funções bases que formam N_j_D são da forma N_x_1 onde x E [i-D+1, i] (se x = i, N_x_1 = 1 para u E [T[i], T[i+1]] )
    #      
    #       b. se j = i + D - 1 então as funções bases que formam N_j_D são da forma N_x_1 onde x E [i, i+D-1] (se x = i, N_x_1 = 1 para u E [T[i], T[i+1]] )
    #
    #       c. se i - D + 1 < j < i é trivial
    #
    # Pode-se notar por essa demonstração que se u E [T[i], T[i+1]] os pontos de controle que influenciam neste segmento da curva são os...
    # ... pontos P[i-D+1], P[i-D+2], P[i-D+3], ..., P[i] ; além disso pode-se notar que a forma como os nós estão sendo montados neste código faz...
    # ... com que a cada segmento tem exatamente a influência de uma quantidade de pontos D-1 se comportando de maneira mais parecida com as...
    # ... curvas Bézier simples. 

    segments = list(set(T))
    print(segments)

    # Obs.: se deixarmos o último valor de u para ser calculado o plot irá ligar o último ponto...
    # ... ao ponto inicial:
    
    # X = [point[0] for point in P[0:-2]]
    # Y = [point[1] for point in P[0:-2]]
    # Z = [point[2] for point in P[0:-2]]

    # (vi) Ajuste de limites do gráfico:
    plt.xlim(-0.5,7)
    plt.ylim(-2,3)

    for i, segment in enumerate(segments[0:-1]):
        piece = [calc_NURBS(points, ui, D, T, weights) for ui in U if segment <= ui <= segments[i+1]]
        X = [point[0] for point in piece[0:-1]]
        Y = [point[1] for point in piece[0:-1]]
        Z = [point[2] for point in piece[0:-1]]

        hexadecimal = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        plt.plot(X, Y, color = hexadecimal)
        
    plt.savefig("Exemplo01-NURBS.png")
    plt.show()
    plt.close()

    print("contador de número etapas (eficiência) = ", counter)