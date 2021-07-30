from matplotlib import pyplot as plt
import numpy as np

def plotter(fn, width=20, duration=100):
  plt.axis([0,width,0,1])
  y=[]
  x=[]
  for i in range(duration):
    y.append(fn(i))
    x.append(i)
    plt.plot(x,y, color='black')
    plt.axis([i-width, i,-1,1])
    plt.autoscale(axis='y')
    plt.pause(0.01)

if __name__ == "__main__":
  # plotter(lambda x : np.sin(2*np.pi*x/100))
  plotter(lambda x : np.sin(x))
