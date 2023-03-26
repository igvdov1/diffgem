import numpy as np
from scipy import integrate
from matplotlib import pyplot as plt 
from itertools import chain


class Point:
    def __init__(self, x: float, y: float, z: float):
     self.x = x
     self.y = y
     self.z = z
    def __truediv__(self, val):
        if type(val) == int or type(val) == float or type(val) == np.float64:
            return Point(self.x / val, self.y / val, self.z / val)
        else:
            raise ValueError("bad type")
    def vector_product(self, other):
        coord1 = (self.x, self.y, self.z)
        coord2 = (other.x, other.y, other.z)
        return Point(coord1[1]*coord2[2] - coord1[2] * coord2[1], 
                -(coord1[0] * coord2[2] - coord1[2]*coord2[0]), 
                coord1[0] * coord2[1] - coord1[1] * coord2[0])
    def scalar_product(self, other):
        coord1 = (self.x, self.y, self.z)
        coord2 = (other.x, other.y, other.z)
        return sum(coord1[i] * coord2[i] for i in range(len(coord1)))
    def length(self):
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)
    def curvature(self, other1, other2):
        temp1 = other1.vector_product(other2).length()
        temp2 = other1.length() **3
        return temp1 / temp2
    def spin(self, other1, other2, other3):
        temp1 = other3.scalar_product((other1.vector_product(other2)))
        temp2 = other1.vector_product(other2).length() **2
        return temp1/temp2
    def speed(self, der_curve):
        return Point(der_curve.x/der_curve.length(),
                     der_curve.y/der_curve.length(),
                     der_curve.z/der_curve.length())
    def normal(self):
        return self.speed.vector_product(self.bi_normal)
    def bi_normal(self, der_curve, sec_der_curve):
        return der_curve.vector_product(sec_der_curve) / der_curve.vector_product(sec_der_curve).length()



class Curve:
    def __init__(self, x: 'function', y: 'function', z: 'function', start: int, finish: int):
        self.x = x
        self.y = y
        self.z = z
        t1 = np.linspace(start, finish, finish * 1000)
        self.points = np.array([Point(x(i), y(i), z(i)) for i in t1])
        self.x_coord = np.array([x(i) for i in t1])
        self.y_coord = np.array([y(i) for i in t1])
        self.z_coord = np.array([z(i) for i in t1])
        self.start = start
        self.finish = finish
        
    
    def visualize(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.plot3D(self.x_coord, self.y_coord, self.z_coord, 'red')
        ax.set_xlabel("x-axis")
        ax.set_ylabel("y-axis")
        ax.set_zlabel("z-axis")
        plt.show()



def x(t):
    return t**2
def y(t):
    return np.exp(t) + 3
def z(t):
    return 3*t + 2

def der_x(t):
    return 2*t
def der_y(t):
    return np.exp(t)
def der_z(t):
    return 3

def sec_der_x(t):
    return 2
def sec_der_y(t):
    return np.exp(t)
def sec_der_z(t):
    return 0

if __name__ == '__main__':
    a = Curve(x, y, z, 0, 100)
    k = [x(1), y(1), z(1)]
    b = Point(*k)
    c = Point(der_x(1), der_y(1), der_z(1))
    d = Point(sec_der_x(1), sec_der_y(1), sec_der_z(1))
    # print(b.speed(c).x, b.speed(c).y, b.speed(c).z)
    print(b.bi_normal(c, d).x, b.bi_normal(c, d).y, b.bi_normal(c, d).z)


    # x = 1
    # y = 2
    # z = 5
    # print(np.sqrt(x**2 + y**2 + z**2))
    # print(b.length())
    # print(c/2)
    # print(b.length())
    # print(integrate.quad(sec_der_x, 0, 2))
