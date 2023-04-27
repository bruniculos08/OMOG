#include <iostream>
#include <stdio.h>
#include <eigen3/Eigen/Dense>
#include <gnuplot-iostream.h>

using namespace Eigen;
using namespace std;

// Uma curva de bezier cúbica é possui 4 pontos de controle, supondo que ela comece em P0 e termine em P3, há também...
// ... os pontos de controle P1 e P2, e portanto no ponto P0, a derivada da curva deve ser o vetor P1-P0 enquanto no...
// ... ponto P3 a derivada é igual ao vetor P3-P2;

int main(void){

}