from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, MovieWriter
import numpy as np

bell = lambda t, mu=1, sigma=0.4, squish=0.8 : squish*np.exp(-0.5*(t-mu)**2/sigma**2)
t = np.arange(0,2,0.01)

def noise(n, samples):
  a = np.random.uniform(size=n)
  box = np.ones(samples)/samples
  return np.convolve(a, box, mode='valid')

fig, ax = plt.subplots()
xdata, ydata = t, []
delta=0.1

slope = lambda x, fn : (fn(x-delta/2) - fn(x + delta/2))/delta
tangentx = np.arange(1-delta, 1+delta, 0.01)
tangenty = slope(tangentx,bell) + bell(tangentx)
ln1, = plt.plot([], [], color='orange')
ln2, = plt.plot([],[], color='red')
plt.title("PDH Technique")
plt.xlabel('Wavelength')
plt.ylabel('Transfer Function')

def init():
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 1)
    return ln1,

# simulated Noise
# def update(frame):
#     ydata = bell(t, mu=0.5+frame, sigma=0.05, squish=0.8)
#     tangenty = slope(
#       1, lambda x : -bell(x, mu=0.5 + frame))*(tangentx - 1) + bell(1, mu=0.5+frame)
#     ln1.set_data(xdata, ydata)
#     ln2.set_data(tangentx, tangenty)
#     return ln1, ln2,
# ani = FuncAnimation(fig, update, frames=noise(100,50),
#                     init_func=init, blit=True)

def update(frame):
    ydata = bell(t, mu=frame, sigma=0.4, squish=0.8)
    tangenty = slope(
      1, lambda x : -bell(x, mu=frame))*(tangentx - 1) + bell(1, mu=frame)
    ln1.set_data(xdata, ydata)
    ln2.set_data(tangentx, tangenty)
    return ln1, ln2,

e = 0; inte = 0; K_p = 0.01; K_i = 0.0002
wavelengths = [0.9]
for i in range(0,30): # iterations become frames in the animation
  # Error is calculated as the slope evaluated at a set point (1)
  e = slope(1, lambda x : bell(x, mu=wavelengths[i]))
  # integral accumulates the error every cycle
  inte += e
  wavelengths.append(
    wavelengths[i]
    +
    K_p*e 
    +
    K_i*inte
    )
  # I've left out the derivative because its especially useless in a noiseless environment

ani = FuncAnimation(fig, update, frames=wavelengths, init_func=init, blit=True)
# plt.show()

ani.save("finale.mp4")
# ani.to_html5_video()
