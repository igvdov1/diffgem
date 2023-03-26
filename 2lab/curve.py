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
    def normal(self, der_curve, sec_der_curve):
        return self.speed(der_curve).vector_product(self.bi_normal(der_curve, sec_der_curve))
    def bi_normal(self, der_curve, sec_der_curve):
        return der_curve.vector_product(sec_der_curve) / der_curve.vector_product(sec_der_curve).length()



class Curve:
    def __init__(self, x: 'function', y: 'function', z: 'function',
                 der_x, der_y, der_z, 
                 sec_der_x, sec_der_y, sec_der_z,
                 thd_der_x, thd_der_y, thd_der_z,
                  start: int, finish: int):
        self.x = x; self.y = y; self.z = z
        self.der_x = der_x; self.der_y = der_y; self.der_z = der_z
        self.sec_der_x = sec_der_x; self.sec_der_y = sec_der_y; self.sec_der_z = sec_der_z
        self.thd_der_x = thd_der_x; self.thd_der_y = thd_der_z; self.thd_der_z = thd_der_z 
        t1 = np.linspace(start, finish, finish * 1000)
        self.x_coord = np.array([x(i) for i in t1])
        self.y_coord = np.array([y(i) for i in t1])
        self.z_coord = np.array([z(i) for i in t1])
        self.start = start
        self.finish = finish
        
    
    def visualize(self, t_values: list):
        fig = plt.figure()
        points = np.array([Point(self.x(i), self.y(i), self.z(i)) for i in t_values])
        der_points = np.array([Point(self.der_x(i), self.der_y(i), self.der_z(i)) for i in t_values])
        points_speed = np.array([i.speed(j) for i, j in zip(points, der_points)])
        
        ax = fig.add_subplot(projection='3d')
        ax.plot3D(self.x_coord, self.y_coord, self.z_coord, 'red')
        # ax.quiver((*points.x)
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

def thd_der_x(t):
    return 0
def thd_der_y(t):
    return np.exp(t)
def thd_der_z(t):
    return 0

if __name__ == '__main__':
    # a = Curve(x, y, z, 0, 100)
    # k = [x(0), y(0), z(0)]
    # b = Point(*k)
    # c = Point(der_x(0), der_y(0), der_z(0))
    # d = Point(sec_der_x(0), sec_der_y(0), sec_der_z(0))
    # print(b.speed(c).x, b.speed(c).y, b.speed(c).z)
    # print(b.bi_normal(c, d).x, b.bi_normal(c, d).y, b.bi_normal(c, d).z)
    # print(type(b.bi_normal(c, d)))
    # print(b.normal(c,d).x, b.normal(c,d).y, b.normal(c,d).z)



    # t = np.linspace(0, 2, 100)
    # x_axis = [x(i) for i in t]
    # y_axis = [y(i) for i in t]
    # z_axis = [z(i) for i in t]
    
    # fig = plt.figure()
    # ax = fig.add_subplot(projection='3d')
    # ax.plot3D(x_axis, y_axis, z_axis, 'red')
    # ax.scatter3D(b.speed(c).x, b.speed(c).y, b.speed(c).z, color = 'green')
    # ax.scatter3D(b.bi_normal(c, d).x, b.bi_normal(c, d).y, b.bi_normal(c, d).z, color = 'yellow')
    # ax.scatter3D(b.normal(c,d).x, b.normal(c,d).y, b.normal(c,d).z)
    # ax.scatter3D(b.x, b.y, b.z, color = 'orange')
    
    # ax.quiver(b.x, b.y, b.z, b.speed(c).x, b.speed(c).y,  b.speed(c).z)
    # ax.quiver(b.x, b.y, b.z, b.normal(c,d).x, b.normal(c,d).y, b.normal(c,d).z, color = 'green')
    # ax.quiver(b.x, b.y, b.z, b.bi_normal(c, d).x, b.bi_normal(c, d).y, b.bi_normal(c, d).z, color = 'yellow')
    # print(b.speed(c).scalar_product(b.normal(c, d)))
    # print(b.speed(c).scalar_product(b.bi_normal(c, d)))
    # print(b.normal(c,d).scalar_product(b.bi_normal(c,d)))
    # ax.set_xlabel("x-axis")
    # ax.set_ylabel("y-axis")
    # ax.set_zlabel("z-axis")
    # plt.show()
    # print(b.bi_normal(c,d).length(), b.normal(c, d).length(), b.speed(c).length())
    # x = 1
    # y = 2
    # z = 5
    # print(np.sqrt(x**2 + y**2 + z**2))
    # print(b.length())
    # print(c/2)
    # print(b.length())
    # print(integrate.quad(sec_der_x, 0, 2))
    a = Point(1, 2, 3)
    b = Point(2, 3, 4)
    k = np.array([a,b])
    print(*k.x)       
    # fig = plt.figure()
    # ax = fig.add_subplot(projection='3d')
    # ax.scatter(*k.x, *k.y, *k.z)
    # plt.show()
