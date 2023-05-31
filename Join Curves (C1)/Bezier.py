import random as random
from math import *
import matplotlib.pyplot as plt
import numpy as np

# Fazendo código para gerar curva de Bezier de grau 2 (3 pontos) em 3 dimensões (mas plotando em 2 por enquanto):

def line_funcs(pA, pB):

    def x_line(u):
        return (pB[0]-pA[0])*u + pA[0]
    
    def y_line(u):
        return (pB[1]-pA[1])*u + pA[1]
    
    def z_line(u):
        return (pB[2]-pA[2])*u + pA[2]
    
    return x_line, y_line, z_line

def build_lerp(p0, p1):
    def lerp_x(u):
        return (1-u)*p0[0] + u*p1[0]    
    def lerp_y(u):
        return (1-u)*p0[1] + u*p1[1]
    def lerp_z(u):
        return (1-u)*p0[2] + u*p1[2] 
    return lerp_x, lerp_y, lerp_z

def lerp(p0, p1, u):
    lerp_x = (1-u)*p0[0] + u*p1[0]
    lerp_y = (1-u)*p0[1] + u*p1[1]
    lerp_z = (1-u)*p0[2] + u*p1[2]
    return [lerp_x, lerp_y, lerp_z]

def calc_bezier(points, u):
    global flag
    
    n = len(points)-1
    for i in range(n, -1, -1):
        for j in range(0, i, 1):
            point = lerp(points[j], points[j+1], u)
            points[j] = point
    
    # Ao final points conterá o ponto calculado na primeira posição (0): 
    return points[0]

def plot_poligon(points):
    plt.rcParams["figure.autolayout"] = True

    i = 0
    for i in range(0, len(points)-1):
        x = [points[i][0], points[i+1][0]] 
        y = [points[i][1], points[i+1][1]]
        plt.plot(x, y, 'bo', linestyle="--")

    plt.rcParams["figure.autolayout"] = False