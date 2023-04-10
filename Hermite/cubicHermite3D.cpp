// Compile and run: g++ cubicHermite3D.cpp -Wall -lboost_iostreams -lm -o cubicHermite3D && ./cubicHermite3D
// Compile and run: g++ cubicHermite3D.cpp -Wall -lboost_iostreams -o cubicHermite3D && ./cubicHermite3D
#include <iostream>
#include <stdio.h>
#include <eigen3/Eigen/Dense>
#include <gnuplot-iostream.h>
#include <vector>
#include <numeric>
#include <random>
#include <memory>

using namespace Eigen;

int degree = 3;
int components_num = 3;
double t[] = {0, 1};

class HermiteCurve3D{
    public:
        MatrixXd Coeffs;

        double calc_X(double t){
            double x = 0;
            for(int i = 0; i < (*this).Coeffs.rows(); i++){
                x += Coeffs(i, 0)*pow(t, degree-i);
            }
            return x;
        }

        double calc_Y(double t){
            double y = 0;
            for(int i = 0; i < (*this).Coeffs.rows(); i++){
                y += Coeffs(i, 1)*pow(t, degree-i);
            }
            return y;
        }

        double calc_Z(double t){
            double z = 0;
            for(int i = 0; i < (*this).Coeffs.rows(); i++){
                z += Coeffs(i, 2)*pow(t, degree-i);
            }
            return z;
        }
        HermiteCurve3D(MatrixXd A);
};

// Obs.: return type may not be specified on a constructorC/C++(963)
HermiteCurve3D::HermiteCurve3D(MatrixXd A){
    (*this).Coeffs = A;

}

MatrixXd cubic_hermite_coeffs(Vector3d p0, Vector3d p1, Vector3d u0, Vector3d u1){
    MatrixXd M(4, 4);
    for(int j = 0; j < degree-1; j++){
        printf("Here\n");
        for(int i = 0; i <= degree; i++) M(j,i) = pow(t[j], degree-i);
        for(int i = 0; i <= degree; i++){
            if(degree-i == 0) M(j+degree-1,i) = 0;
            else M(j+degree-1,i) = (degree-i)*pow(t[j], degree-i-1);
        }
    }

    MatrixXd points_and_tangents(degree+1, components_num);
    for(int j = 0; j < components_num; j++){
        points_and_tangents(0, j) = p0(j);
        points_and_tangents(1, j) = p1(j);
        points_and_tangents(2, j) = u0(j);
        points_and_tangents(3, j) = u1(j);
    }

    std::cout << "The points_and_tangents is:\n" << points_and_tangents << std::endl;
    std::cout << "The M is:\n" << M << std::endl;
    MatrixXd result(degree+1, components_num);
    result = M.colPivHouseholderQr().solve(points_and_tangents);
    return result;

}

int main(void){
    Vector3d p0(0,0,0);
    Vector3d p1(0,1,0);
    Vector3d u0(2,5,0);
    Vector3d u1(2,-5,0);
    MatrixXd result(degree+1, components_num);
    result = cubic_hermite_coeffs(p0, p1, u0, u1);
    std::cout << "The solution is:\n" << result << std::endl;

    HermiteCurve3D curve(result);  
    // double ti = 1;  
    // std::cout << "P(" << ti << ") = (" << curve.calc_X(ti) << ", " << curve.calc_Y(ti) << ", " << curve.calc_Z(ti) << ")" << std::endl;

    int num_of_points = 1000;
    std::vector<double> x_points;
    std::vector<double> y_points;
    std::vector<double> z_points;
    double ti = 0;
    for(int i = 0; i < num_of_points; i++){
        x_points.push_back(curve.calc_X(ti));
        y_points.push_back(curve.calc_Y(ti));
        z_points.push_back(curve.calc_Z(ti));
        ti += 1.0/num_of_points;
    }

    Gnuplot gp("gnuplot");
    // // Obs.: por enquanto estou plotando em 2D.
    gp << "set title 'Graph of hermite curve'\n";

    std::vector<std::pair<double, double>> x_y_points;
    for(int i = 0; i < num_of_points; i++){
        x_y_points.push_back(std::make_pair(x_points[i], y_points[i]));

    }

    gp << "plot '-'  with lines title 'points'\n";
    gp.send1d(x_y_points);


    // falta ainda plotar os vetores tangentes
    std::cin.get();
}