import numpy as np
from matplotlib import pyplot as plt
from curve import Point



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

def paint(k):
    
    b = Point(*k)
    c = Point(der_x(0), der_y(0), der_z(0))
    d = Point(sec_der_x(0), sec_der_y(0), sec_der_z(0))
    print(b.speed(c).x, b.speed(c).y, b.speed(c).z)
    print(b.bi_normal(c, d).x, b.bi_normal(c, d).y, b.bi_normal(c, d).z)
    print(type(b.bi_normal(c, d)))
    print(b.normal(c,d).x, b.normal(c,d).y, b.normal(c,d).z)



    t = np.linspace(0, 2, 100)
    x_axis = [x(i) for i in t]
    y_axis = [y(i) for i in t]
    z_axis = [z(i) for i in t]

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.plot3D(x_axis, y_axis, z_axis, 'red')
    
    ax.quiver(b.x, b.y, b.z, b.speed(c).x, b.speed(c).y,  b.speed(c).z)
    ax.quiver(b.x, b.y, b.z, b.normal(c,d).x, b.normal(c,d).y, b.normal(c,d).z, color = 'green')
    ax.quiver(b.x, b.y, b.z, b.bi_normal(c, d).x, b.bi_normal(c, d).y, b.bi_normal(c, d).z, color = 'yellow')
    print(b.speed(c).scalar_product(b.normal(c, d)))
    print(b.speed(c).scalar_product(b.bi_normal(c, d)))
    print(b.normal(c,d).scalar_product(b.bi_normal(c,d)))
    ax.set_xlabel("x-axis")
    ax.set_ylabel("y-axis")
    ax.set_zlabel("z-axis")

    plt.show()
if __name__ == '__main__':
    
    k = [x(0), y(0), z(0)]
    paint(k)