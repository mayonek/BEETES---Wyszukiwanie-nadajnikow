import pandas as pd
import numpy as np
df = pd.read_csv('btsx.csv', dtype = {'LAT': np.float64, 'LON': np.float64, 'Adres': np.str, })
import math
def closest(lst, K):
    lst = np.asarray(lst)
    idx = (np.abs(lst - K)).argmin()
    return lst[idx]
def closest2(lst2, K2):
    lst2 = np.asarray(lst2)
    idx = (np.abs(lst2 - K2)).argmin()
    return lst[idx]
lst = df['LAT']
lst2 = df['LON']
K = 50
K2 = 20
print(closest(lst, K))
print(closest(lst2, K2))
x1 = 50.21012
y1 = 19.124151
x2 = (closest(lst2, K2))
y2 = (closest(lst2, K2))


def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * 100
    return dist


print("Odległość: %.2fKM" % float(calculateDistance(x1, y1, x2, y2)))
