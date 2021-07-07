import numpy as np
from matplotlib import pyplot as plt
# from numpy.core.numeric import convolve

# # def noise(n):
# #   buffer = list(np.ones(5)/2)
# #   for i in range(n):
# #     mean = sum(buffer)/len(buffer)
# #     buffer.pop(0)
# #     buffer.append(np.random.uniform(0,1))
# #     yield mean

# def noise(n, samples):
#   a = np.random.uniform(size=n)
#   box = np.ones(samples)/samples
#   return np.convolve(a, box, mode='valid')

# # out = noise(100)
# # print(list(out))
# plt.plot(noise(100000,1000))
# plt.show()


