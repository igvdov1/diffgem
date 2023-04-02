from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
from curve import Point
import scipy.integrate as integrate 

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




# plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams['text.usetex'] = True
fig = plt.figure(figsize = (16, 16))
fig.text(0.5, 0.0, 
         f"length = {integrate.quad(lambda t: ((2 * t)**2 + np.exp(t) ** 2 + 9)**(1/2), 0, 4)}", 
         style = 'italic',
         fontsize = 10,
         color = "black")
ax1 = fig.add_subplot(122, projection='3d')
ax2 = fig.add_subplot(321)
ax3 = fig.add_subplot(323)
ax4 = fig.add_subplot(325)


b1 = Point(x(0), y(0), z(0))
c1 = Point(der_x(0), der_y(0), der_z(0))
d1 = Point(sec_der_x(0), sec_der_y(0), sec_der_z(0))
t = np.linspace(0, 4, 100)

# Setting the axes properties
ax1.set_xlim3d([b1.x - 1, b1.x+ 4])
ax1.set_xlabel('X')
ax1.set_ylim3d([b1.y - 1, b1.y+6])
ax1.set_ylabel('Y')
ax1.set_zlim3d([b1.z - 1, b1.z+6])
ax1.set_zlabel('Z')
ax2.set_xlim((0, 4))
ax2.set_ylim((-1, 1))
ax3.set_xlim((0, 4))
ax3.set_ylim((-1, 1))
ax4.set_xlim((0, 4))
ax4.set_ylim((-1, 1))

#title
ax1.set_title('Curve, with reper Frene')
ax2.set_title('Point of parametrization')
ax3.set_title('Curvature')
ax4.set_title('Spin')
plt.subplot_tool()



def gen(n):
    """Curve generator."""
    phi = 0
    t = np.linspace(0, 4, n)
    for phi in t:
        b1 = Point(x(phi), y(phi), z(phi))
        yield np.array([b1.x, b1.y, b1.z])

def gen1(n):
    """Curve of the first derivative generator."""
    phi = 0
    t = np.linspace(0, 4, n)
    for phi in t:
        c1 = Point(der_x(phi), der_y(phi), der_z(phi))
        yield np.array([c1.x, c1.y, c1.z])

def gen2(n):
    """Curve of the double derivative generator."""
    phi = 0
    t = np.linspace(0, 4, n)
    for phi in t:
        d1 = Point(sec_der_x(phi), sec_der_y(phi), sec_der_z(phi))
        yield np.array([d1.x, d1.y, d1.z])


def update(num, data, data1, data2, line, points, curvature_data, spin_data, curvature_line, spin_line):
    """frame-by-frame generator"""
    fig.suptitle(f'frame = {num}')
    global vector_speed, vector_normal, vector_bi_normal, t, parametrization_point, curvature_point, spin_point
#ax1
    line.set_data(data[:2, :num])
    line.set_3d_properties(data[2, :num])

    points.set_data(data[:2, num-1:num])
    points.set_3d_properties(data[2, num-1:num])

    b1 = Point(data[0, num-1:num], data[1, num-1:num], data[2, num-1:num])
    c1 = Point(data1[0, num-1:num], data1[1, num-1:num], data1[2, num-1:num])
    d1 = Point(data2[0, num-1:num], data2[1, num-1:num], data2[2, num-1:num])



    if c1.x.size > 0 and c1.vector_product(d1).length():
        print(c1.vector_product(d1).length(),
          f'c1x = {c1.x}, c1y = {c1.y}, c1z = {c1.z}\n',
          f'd1x = {d1.x}, d1y = {d1.y}, d1z = {d1.z}\n',
          f'b1x = {b1.x}, b1y = {b1.y}, b1z = {b1.z}\n',
          f'vector_product = {c1.vector_product(d1)}\n',
          f'vector_product = {c1.vector_product(d1).length()[0]}'
          )
        bi_normal = c1.vector_product(d1)/c1.vector_product(d1).length()[0]
        normal = b1.speed(c1).vector_product(bi_normal)
        vector_normal.remove()
        vector_normal = ax1.quiver(b1.x, b1.y, b1.z, normal.x, normal.y, normal.z, color = 'green')
        vector_bi_normal.remove()
        vector_bi_normal = ax1.quiver(b1.x, b1.y, b1.z, bi_normal.x, bi_normal.y, bi_normal.z, color = 'yellow')
    vector_speed.remove()
    vector_speed = ax1.quiver(b1.x, b1.y, b1.z, b1.speed(c1).x, b1.speed(c1).y,  b1.speed(c1).z, color = 'purple')    

#ax2
    parametrization_point.remove()
    parametrization_point = ax2.scatter(t[num], 0, color = 'red')

#ax3
    curvature_line.set_data(t[:num], curvature_data[:num])
    curvature_point.remove()
    curvature_point = ax3.scatter(t[num], curvature_data[num], color = 'red')

#ax4
    spin_line.set_data(t[:num], spin_data[:num])
    spin_point.remove()
    spin_point = ax4.scatter(t[num], spin_data[num], color = 'red')


N = 100

#ax1
data = np.array(list(gen(N))).T
data1 = np.array(list(gen1(N))).T
data2 = np.array(list(gen2(N))).T
line, = ax1.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1], lw = 4)
points, = ax1.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1], '.')
vector_speed = ax1.quiver(data[0, 0:1], data[1, 0:1], data[2, 0:1], b1.speed(c1).x, b1.speed(c1).y,  b1.speed(c1).z, color = 'purple')
vector_normal = ax1.quiver(data[0, 0:1], data[1, 0:1], data[2, 0:1], b1.normal(c1,d1).x, b1.normal(c1,d1).y, b1.normal(c1,d1).z, color = 'green')
vector_bi_normal = ax1.quiver(data[0, 0:1], data[1, 0:1], data[2, 0:1], b1.bi_normal(c1, d1).x, b1.bi_normal(c1, d1).y, b1.bi_normal(c1, d1).z, color = 'yellow')


#ax 2
parametrization_line = ax2.plot(t, [0] * len(t))
parametrization_point = ax2.scatter(t[0], 0, color = 'red')

#extra data
b2 = np.array([Point(x(i), y(i), z(i)) for i in t])
c2 = np.array([Point(der_x(i), der_y(i), der_z(i)) for i in t])
d2 = np.array([Point(sec_der_x(i), sec_der_y(i), sec_der_z(i)) for i in t])
f2 = np.array([Point(thd_der_x(i), thd_der_y(i), thd_der_z(i)) for i in t])
curvature_data = [b2[i].curvature(c2[i], d2[i]) for i in range(len(t))]
spin_data = [b2[i].spin(c2[i], d2[i], f2[i]) for i in range(len(t))]

#ax3
curvature_line, = ax3.plot(t[0], curvature_data[0])
curvature_point = ax3.scatter(t[0], curvature_data[0], color = 'red')

#ax4 
spin_line, = ax4.plot(t[0], spin_data[0])
spin_point = ax4.scatter(t[0], spin_data[0], color = 'red')

ani = animation.FuncAnimation(fig, update, N, fargs=(data, data1, data2, line, points, curvature_data, spin_data, curvature_line, spin_line), interval=10000/N, blit=False)
ani.save('2lab/Frene_deformation.gif', writer='imagemagick')
plt.show()