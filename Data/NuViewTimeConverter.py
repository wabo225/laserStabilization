import numpy as np
from typing import Tuple
from sys import argv, path
import re
import os.path
from datetime import datetime

def extractHMS(datestring: str) -> Tuple[int, int, float]: 
    '''

    This function uses Regular Expressions to separate out the hour, minute, 
        seconds, and millisecond values from a date string format used in Bristol's
        Wavemeter.
    
    Dates are formatted as: 2021-07-27T14:19:41.147
    
    They are found in the first column of the csv, below the column header 
        labelled Timestamp
    
    @param datestring: str
    @returns: Tuple[int, int, float]  The entries are hours: int, minutes; int, seconds: float

    @todo: this function is coupled with timeTupleToSeconds(), a function that is unlikely to be reused.
    '''
    r = re.search(r'^.*T(\d\d):(\d\d):(\d\d).(\d\d\d)', datestring)
    return int(r.group(1)), int(r.group(2)), round(int(r.group(3)) + int(r.group(4))/1000,3)

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

def NuViewTimeConverter(pathToFile: str):
    '''
        This function requires a file formatted by the 
    '''
    if not os.path.isfile(pathToFile):
        print("\n You've given an invalid filename \n")
        return
    
    with open(pathToFile) as f:
        header = f.readline()
        data = np.genfromtxt(f,dtype=str, delimiter=',')
        secondsColumn = [BristolTimestampToPOSIX(timestamp) for timestamp in data[:,0]]
        secondsColumn = [round(second-secondsColumn[0],3) for second in secondsColumn]
        data[:,0] = secondsColumn
    
    with open(pathToFile.split('.csv')[0] + ' (copy).csv', 'w') as f:
        f.write(header)
        for row in data:
            for cell in row:
                f.write(f'{cell}, ')
            f.write('\n')

if __name__ == "__main__":
    if len(argv) != 2:
        print("\nYou need to specify a file to convert")
        print("     Example : python NuViewTimeConverter.py \"NuView log 10.csv\"\n")
    else:
        NuViewTimeConverter(argv[1])
        print(f'\nYour file was created at: {argv[1].split(".csv")[0]} (copy).csv\n')