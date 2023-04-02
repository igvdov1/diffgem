from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
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



fig = plt.figure()
ax = fig.add_subplot(projection='3d')
t = np.linspace(0, 4, 100)
def gen(n):
    phi = 0
    t = np.linspace(0, 4, n)

    for phi in t:
        b1 = Point(x(phi), y(phi), z(phi))
        yield np.array([b1.x, b1.y, b1.z])

def gen1(n):
    phi = 0
    t = np.linspace(0, 4, n)

    for phi in t:
        c1 = Point(der_x(phi), der_y(phi), der_z(phi))
        yield np.array([c1.x, c1.y, c1.z])

def gen2(n):
    phi = 0
    t = np.linspace(0, 4, n)

    for phi in t:
        d1 = Point(sec_der_x(phi), sec_der_y(phi), sec_der_z(phi))
        yield np.array([d1.x, d1.y, d1.z])


def update(num, data, data1, data2, line, points):
    line.set_data(data[:2, :num])
    line.set_3d_properties(data[2, :num])
    
    # update properties
    points.set_data(data[:2, num-1:num])
    points.set_3d_properties(data[2, num-1:num])
    b1 = Point(data[0, num-1:num], data[1, num-1:num], data[2, num-1:num])
    # c1 = Point(*data1[num-1:num])
    
    c1 = Point(data1[0, num-1:num], data1[1, num-1:num], data1[2, num-1:num])
    d1 = Point(data2[0, num-1:num], data2[1, num-1:num], data2[2, num-1:num])
    # print(b1.bi_normal(c1, d1))
    # print()
    global vector_speed, vector_normal, vector_bi_normal
    # e1 = b1.bi_normal(c1, d1)
    vector_speed.remove()
    # vector_normal.remove()
    vector_speed = ax.quiver(b1.x, b1.y, b1.z, b1.speed(c1).x, b1.speed(c1).y,  b1.speed(c1).z, color = 'purple')    
    # vector_bi_normal = ax.quiver(b1.x, b1.y, b1.z, 3, 3, 3, color = 'yellow')
    # vector_normal = ax.quiver(b1.x, b1.y, b1.z, b1.normal(c1,d1).x, b1.normal(c1,d1).y, b1.normal(c1,d1).z, color = 'green')
    # print(c1.x)
    

b1 = Point(x(0), y(0), z(0))
c1 = Point(der_x(0), der_y(0), der_z(0))
d1 = Point(sec_der_x(0), sec_der_y(0), sec_der_z(0))


N = 100
data = np.array(list(gen(N))).T
data1 = np.array(list(gen1(N))).T
data2 = np.array(list(gen2(N))).T
line, = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1], lw = 4)
points, = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1], '.')
vector_speed = ax.quiver(data[0, 0:1], data[1, 0:1], data[2, 0:1], b1.speed(c1).x, b1.speed(c1).y,  b1.speed(c1).z, color = 'purple')
vector_normal = ax.quiver(data[0, 0:1], data[1, 0:1], data[2, 0:1], b1.normal(c1,d1).x, b1.normal(c1,d1).y, b1.normal(c1,d1).z, color = 'green')
vector_bi_normal = ax.quiver(data[0, 0:1], data[1, 0:1], data[2, 0:1], b1.bi_normal(c1, d1).x, b1.bi_normal(c1, d1).y, b1.bi_normal(c1, d1).z, color = 'yellow')

# Setting the axes properties
ax.set_xlim3d([b1.x - 1, b1.x+ 4])
ax.set_xlabel('X')

ax.set_ylim3d([b1.y - 1, b1.y+6])
ax.set_ylabel('Y')

ax.set_zlim3d([b1.z - 1, b1.z+6])
ax.set_zlabel('Z')

ani = animation.FuncAnimation(fig, update, N, fargs=(data, data1, data2, line, points), interval=10000/N, blit=False)
ani.save('Frene_deformation.gif', writer='imagemagick')
plt.show()