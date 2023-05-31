from Bezier import *
from BSplineDynamic import *
import numpy as np

def plot_BSpline(points):

    n = len(points)-1
    D = 4

    T = getKnots(n, D)
    print(T)

    plot_poligon(points)
    U = np.linspace(0.0, n-D+2, 1000)

    segments = list(set(T))
    print(segments)

    for i, segment in enumerate(segments[0:-1]):
        piece = [calc_BSpline(points, ui, D, T) for ui in U if segment <= ui <= segments[i+1]]
        X = [point[0] for point in piece[0:-1]]
        Y = [point[1] for point in piece[0:-1]]
        Z = [point[2] for point in piece[0:-1]]

        hexadecimal = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        plt.plot(X, Y, color = hexadecimal)


def plot_Bezier(points):

    plot_poligon(points)
    U = np.linspace(0, 1, 1000)
    P = [calc_bezier(points, ui) for ui in U]
    
    X = [point[0] for point in P]
    Y = [point[1] for point in P]
    Z = [point[2] for point in P]
    
    plt.plot(X, Y, color = "blue")
    

def translate(points, delta_x, delta_y, delta_z):
    for point in points:
        point[0] += delta_x
        point[1] += delta_y
        point[2] += delta_z
    return points

"""
Função que retorna um vetor, dados dois pontos p0 e p1
"""
def calc_vector(p0, p1):
    v = [p1[0]-p0[0], p1[1]-p0[1], p1[2]-p0[2]]
    return v


"""
Função equivalente a aplicar a matriz de rotação no eixo z
"""
def rotate_z_axis(points, alpha):
    for point in points:
        point[0] = cos(alpha)*point[0] - sin(alpha)*point[1]
        point[1] = sin(alpha)*point[0] + cos(alpha)*point[1]
    return points

"""
Função que realiza produto vetorial <v0, v1> considerando apenas as coordenadas x e y
para que possamos calcular o angulô entre as componentes dos vetores <v0, v1> no plano xy 
"""
def dot_product_xy(v0, v1) -> float:
    x0 = v0[0]
    x1 = v1[0]
    y0 = v0[1]
    y1 = v1[1]
    return x0*x1 + y0*y1

"""
Função para cálculo da magnitude da componente de um vetor v sobre o plano xy
"""
def mag_vector_xy(v) -> float:
    return sqrt(v[0]**2 + v[1]**2)

"""
Função para cálculo do ângulo entre as compontes dos vetores v0 e v1 no plano xy
"""
def calc_angle_xy(v0, v1) -> float:
    numerator = dot_product_xy(v0, v1)
    denominator = mag_vector_xy(v0) * mag_vector_xy(v1)
    cosseno = abs(numerator/denominator)
    return np.arccos(cosseno)


"""
Função que ajusta o ângulo entre os pontos de controle de uma curva 1 e 2 para 
obter G1 em relação ao plano xy
"""
def ajust_control_points(points_0, points_1):
    v0 = calc_vector(points_0[-2], points_0[-1])
    v1 = calc_vector(points_0[-1], points_1[1])

    alpha = calc_angle_xy(v0, v1)
    print("alpha = ", alpha)

    initial_point = list(points_1[0])

    translated_points = points_1
    # É necessário colocar os pontos da curva sobre a origem para rotacioná-la:
    translated_points = translate(translated_points, -initial_point[0], -initial_point[1], -initial_point[2])
    
    translated_points = rotate_z_axis(translated_points, -alpha)

    points_1 = translate(translated_points, initial_point[0], initial_point[1], initial_point[2])


    return points_1


if __name__ == '__main__':

    bspline_points = [[0, 0, 0], [0.5, 1.5, 0], [1.25, 2, 0],
                        [2.5, 1.5, 0], [1.5, 0.5, 0], [4, -1.5, 0], 
                        [4, 0, 0], [5, 1, 0], [6, 2, 0]]

    # Exemplo da função que calcular curvas de bezier para quaisquer número n+1 de pontos:
    # Obs.: o grau é igual ao número de pontos menos um, isto é, n.
    bezier_points = [[0, 0, 0], [0.5, 2, 0], [1.25, 2, 0],
                     [2.5, 1.5, 0], [1.5, 0.5, 0], [4, -1.5, 0], 
                     [4, 0, 0], [5, 1, 0]]

    delta = calc_vector(bezier_points[0], bspline_points[-1])

    bezier_points = translate(bezier_points, delta[0], delta[1], delta[2])
    bezier_points = ajust_control_points(bspline_points, bezier_points)

    print(bspline_points)
    print(bezier_points)

    plt.xlim(-1,12)
    plt.ylim(-2,8)

    plot_Bezier(bezier_points)
    plot_BSpline(bspline_points)


    plt.savefig("Exemplo-Join-BSpline-Bezier.png")
    plt.show()
    plt.close()