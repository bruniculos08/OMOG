from Bezier import *
from BSplineDynamic import *

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


def calc_vector(p0, p1):
    v = [p1[0]-p0[0], p1[1]-p0[1], p1[2]-p0[2]]
    return v


if __name__ == '__main__':

    bspline_points = [[0, 0, 0], [0.5, 1.5, 0], [1.25, 2, 0],
                        [2.5, 1.5, 0], [1.5, 0.5, 0], [4, -1.5, 0], 
                        [4, 0, 0], [5, 1, 0], [6, 3, 0]]

    # Exemplo da função que calcular curvas de bezier para quaisquer número n+1 de pontos:
    # Obs.: o grau é igual ao número de pontos menos um, isto é, n.
    bezier_points = [[0, 0, 0], [0.5, 1.5, 0], [1.25, 2, 0],
                     [2.5, 1.5, 0], [1.5, 0.5, 0], [4, -1.5, 0], 
                     [4, 0, 0], [5, 1, 0]]

    delta = calc_vector(bezier_points[0], bspline_points[-1])

    bezier_points = translate(bezier_points, delta[0], delta[1], delta[2])

    print(bezier_points)

    plt.xlim(-1,12)
    plt.ylim(-2,7)

    plot_Bezier(bezier_points)
    plot_BSpline(bspline_points)

    plt.savefig("Exemplo-Join-BSpline-Bezier.png")
    plt.show()
    plt.close()