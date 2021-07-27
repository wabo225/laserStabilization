from os import listdir
import re

pathToData = '../Data/FrequencyDrift/'

def getNextTrialNumber(pathToData: str):
    trials = filter(lambda filename : filename.find('trial') != -1, listdir(pathToData))
    indices = [int(re.search(r'.*trial(\d*', trial).group(1)) for trial in trials]
    return max(indices) + 1

print(getNextTrialNumber(pathToData))