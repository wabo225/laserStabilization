from matplotlib import pyplot as plt
import numpy as np
import time

def plotter(fn, *args, width:int=20, duration:int=100, callback=lambda : None):
  '''
  @param fn: function   Give the function to call to get data. Must return a single float
    @todo allow fn to return multiple values, plotting each as its own line. Takes no parameters
  @param width: int 
  @param duration: int
  @callback function    This function is passed any *args, and can be used to set parameters on the laser or anything else. It is called every loop
  '''
  plt.axis([0,width,0,1])
  y=[]
  x=[]
  ts=[]
  start = time.time()
  for i in range(duration):
    callback(i, *args)
    y.append(fn())
    t = time.time()
    ts.append(t - start)
    x.append(i)
    plt.plot(x, y, color='black')
    # for j in range(len(*args)):
    #   pass
    plt.axis([i-width, i,-1,1])
    plt.autoscale()
    plt.pause(0.02)
  return np.array([ts,y]).transpose()

if __name__ == "__main__":
  # plotter(lambda x : np.sin(2*np.pi*x/100))
  plotter(lambda x : np.sin(x))
