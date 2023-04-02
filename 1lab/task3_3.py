import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#r << R
def initpict():
    line1.set_data([], [])

    pc.center=(0,0)
    ax.add_patch(pc)
    pp.center=(0,R+r)
    ax.add_patch(pl)
    pl.center = (0, R)
    ax.add_patch(pp)
    return pc,pp, pl, line1
def redraw(i):
    global x
    teta = r/R * i/180 * math.pi
 
    i = math.radians(i)
    plt.title(f'i = {i}')
    ro = math.sqrt((R + r) ** 2 + r ** 2 - 2 * math.cos(i) * (R + r) * r)

    phi = teta - math.asin(r/ro * math.sin(i))
    
    
    x = ro * math.cos(phi)
    
    
    
    y = ro * math.sin(phi)
    xc = (R + r) * math.cos(teta)
    yc = (R + r) * math.sin(teta)
    # plt.scatter(x,y)
    pp.center = (xc, yc)
    pc.center = (0, 0)
    pl.center = (x, y)
    xdata.append(x)
    ydata.append(y)
    line1.set_data(xdata, ydata)

    return pc,pp,pl,line1



r = 0.5
R = 1


fig = plt.figure()
fig.set_dpi(200)

ax = plt.axes(xlim=(-(R + 2 * r + 2), R + 2 * r + 2 ), ylim=(- (R + 2 * r + 2), R + 2 * r + 2))
x = 0
line1, = ax.plot([], [] ,lw=2)

xdata = []
ydata = [] 
pc = plt.Circle((0, 0), R, fc='purple')
pp = plt.Circle((0, 0), r, fc='green')
pl = plt.Circle((0, R), r /10, color = 'red')
ax.set_aspect('equal')
anim =animation.FuncAnimation(fig, redraw, init_func=initpict,
frames= 720, interval=20, blit=True)
plt.show()
anim.save('circle_on_circle_r<<R.gif', writer='Pillow')