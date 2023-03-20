import numpy as np

class Curve:
    def __init__(self, x: 'function', y: 'function', z: 'function', t: int):
        self.x = x
        self.y = y
        self.z = z
        t1 = np.linspace(0, t, t * 1000)
        self.x_axes = np.array([x(i) for i in t1])
        self.y_axes = np.array([y(i) for i in t1])
        self.z_axes = np.array([z(i) for i in t1])
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
    a = Curve(x, y, z, 5)
    print(a.scalar_product)


