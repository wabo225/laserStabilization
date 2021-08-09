import numpy as np
from sys import argv
import re
from datetime import datetime
import os

def BristolTimestampToPOSIX(datestring: str) -> float:
    '''
    This function uses Regular Expressions to convert a date string format used in Bristol's
        Wavemeter to seconds since the Epoch
    
    Dates are formatted as: 2021-07-27T14:19:41.147
    
    They are found in the first column of the csv, below the column header 
        labelled Timestamp
    
    @param datestring: str
    @returns: float  seconds since the Epoch

    '''
    r = re.search(r'(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)\.(\d\d\d)', datestring)
    if r==None:
        raise ValueError("Your Timestamp may not fit the Bristol format. Got: " + datestring)
    dateTuple = [int(r.group(i)) for i in range(1, 7)] + [int(r.group(7))*1000]
    return datetime(*dateTuple).timestamp()

def openBristolFile(pathToFile: str) -> np.ndarray:
    '''
        This function requires a file formatted by the Bristol wavemeter gui, NuView. In NuView we generate .csv files by pressing File > record (or Alt > Enter > Down > Enter > Enter)

        The file has a first column of timestamps, and optional second, third and fourth columns with headers signifying their contents.

        @param pathToFile: str  path to file formatted as a NuView Recording csv
    '''
    if not os.path.isfile(pathToFile):
        print("\n You've given an invalid filename \n")
        raise FileExistsError
    with open(pathToFile) as f:
        header = f.readline()
        data = np.genfromtxt(f,dtype=str, delimiter=',')
        secondsColumn = [BristolTimestampToPOSIX(timestamp) for timestamp in data[:,0]]
        secondsColumn = [round(second-secondsColumn[0],3) for second in secondsColumn]
        data[:,0] = secondsColumn
        
    
    return data.astype('float64')

if __name__ == "__main__":
  from matplotlib import pyplot as plt
  d = openBristolFile(argv[1])
  plt.plot(d[:,0],d[:,1])
  plt.show()
  
      
  
  
  
  