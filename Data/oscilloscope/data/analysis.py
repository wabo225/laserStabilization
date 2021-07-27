from __future__ import with_statement
import numpy as np
from scipy import stats
from os import listdir, stat

search : str = 'TOF'

def callback(file_name: str):
  return file_name.endswith('.csv') and file_name.find(search) != -1

files = list(filter(callback, listdir()))
print(files)
for csv in files:
  with open('./'+csv, 'r') as f:
    # print(f.readlines(5))
    print(*[f.readline() for i in range(5)])
    columns = f.readline().split(',')
    dat = np.reshape(np.fromfile(f,sep=','),(-1,len(columns)))
    print(stats.ttest_1samp(dat[:,1],0))


    