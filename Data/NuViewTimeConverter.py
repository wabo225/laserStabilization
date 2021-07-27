from itertools import groupby
from posixpath import sep
import numpy as np
from typing import Tuple
from sys import argv
import re

from numpy.core.defchararray import rpartition

def extractHMS(datestring: str) -> Tuple[int, int, float]: 
    r = re.search(r'^.*T(\d\d):(\d\d):(\d\d).(\d\d\d)', datestring)
    return int(r.group(1)), int(r.group(2)), round(int(r.group(3)) + int(r.group(4))/1000,3)

def timeTupleToSeconds(time: Tuple[int, int, float]) -> float:
    return 3600*time[0] + 60*time[1] + time[2]

def main():
    with open(argv[1]) as f:
        header = f.readline()
        data = np.genfromtxt(f,dtype=str, delimiter=',')
        secondsColumn = [timeTupleToSeconds(extractHMS(date)) for date in data[:,0]]
        secondsColumn = [round(second-secondsColumn[0],3) for second in secondsColumn]
        data[:,0] = secondsColumn
    with open(argv[1], 'w') as f:
        f.write(header)
        for row in data:
            for cell in row:
                f.write(f'{cell}, ')
            f.write('\n')

if __name__ == "__main__":
    main()