import numpy as np


class Point:
    def __init__(self, x: float, y: float, z: float):
     self.x = x
     self.y = y
     self.z = z
class Curve:
    def __init__(self, x: 'function', y: 'function', z: 'function', start: int, finish: int):
        self.x = x
        self.y = y
        self.z = z
        t1 = np.linspace(start, finish, finish * 1000)
        self.points = np.array(Point(x[i], y[i], z[i]) for i in t1)
        
    def vector_product(self, other, t):
        coord1 = (self.x(t), self.y(t), self.z(t))
        coord2 = (other.x(t), other.y(t), other.z(t))
        return (coord1[1]*coord2[2] - coord1[2] * coord2[1], 
                -(coord1[0] * coord2[2] - coord1[2]*coord2[0]), 
                coord1[0] * coord2[1] - coord1[1] * coord2[0])
    def scalar_product(self, other, t):
        coord1 = (self.x(t), self.y(t), self.z(t))
        coord2 = (other.x(t), other.y(t), other.z(t))
        return (coord1[i] * coord2[i] for i in range(len(coord1)))
    

def x(t):
    return t**2
def y(t):
    return t + 3
def z(t):
    return 3*t + 2


if __name__ == '__main__':
    a = Curve(x, y, z,0, 1)
    print(a.points[0])

