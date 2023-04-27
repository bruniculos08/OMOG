import random as random
from math import *
import matplotlib.pyplot as plt
import numpy as np

def cubic_hermite_coeffs(p0, p1, u0, u1, t):
    # Iremos supor que o parâmetro t varia restrito ao intervalo [t0, t1]
    T = []
    # O range poderia variar de 0 à 4 pois temos 4 equações para cada variável (e portanto 4 linhas na matriz T),...
    # ... mas como temos que tratar de equações com formatos diferentes vamos fazer dois laços cobrindo metade do range cada:
    for i in range(0, 2): 
        T_line = []
        for j in range(0, 4):
            value = t[i]**(3-j)
            T_line.append(value)
        T.append(T_line)
    
    for i in range(0, 2): 
        T_line = []
        for j in range(0, 4):
            value = (3-j)*t[i]**(abs(2-j))
            T_line.append(value)
        T.append(T_line)

    print("T:")
    print(T)

    # Iremos montar agora a matriz que contém os valores do lado direito da equação matricial que montamos na folha;
    Coords_and_Vectors = [[], [], [], []]
    for i in range(0, 3):
        Coords_and_Vectors[0].append(p0[i])
        Coords_and_Vectors[1].append(p1[i])
        Coords_and_Vectors[2].append(u0[i])
        Coords_and_Vectors[3].append(u1[i])

    print("Cord and Vectors:")
    print(Coords_and_Vectors)

    # Note que os coeficientes de cada coordenada, na matriz escalonada estão na coluna referente a respectiva coordenada:
    return np.linalg.solve(T, Coords_and_Vectors)

def build_func(coeffs):
    def f(t):
        x = 0
        y = 0
        z = 0
        for i in range(len(coeffs), 0, -1):
            x += coeffs[len(coeffs) - i][0]*(t**(i-1))
            y += coeffs[len(coeffs) - i][1]*(t**(i-1))
            z += coeffs[len(coeffs) - i][2]*(t**(i-1))
        return [x, y, z]
    return f


if __name__ == '__main__':
    p0 = [0, 0, 0]
    p1 = [0, 1, 0]
    u0 = [2, 5, 0]
    u1 = [2, -5, 0]
    coeffs = cubic_hermite_coeffs(p0, p1, u0, u1, [0, 1])

    print(coeffs)

    f = build_func(coeffs)

    extra_interval = 5
    t = np.linspace(0-extra_interval, 1+extra_interval, 1000)
    fx = [f(ti)[0] for ti in t]
    fy = [f(ti)[1] for ti in t]

    data = np.array([u0[0:2], u1[0:2]])
    origin = np.array([[p0[0], p1[0]], [p0[1], p1[1]]])
    plt.quiver(*origin, data[:, 0], data[:, 1], color=['black', 'red', 'green'], scale=40)

    # plt.xlim(-0.5,1)
    # plt.ylim(0,2)
    plt.plot(fx, fy, label = "blue")
    plt.savefig("Hermite.png")
    plt.show()
    plt.close()