from  geopy.geocoders import Nominatim
import substring
import xlrd
import time
import pandas as pd
import numpy as np
import math
# Śląsk,Dolnyślask,Małopolska,Opolskie
geolocator = Nominatim(user_agent="my-application")
loadbarwidth = 23
print("################################################")
print("BE TE ESIK v0.01 by piotr.wawrzyczek@netia.pl")
print("Śląsk, Dolnyśląsk, Małopolska, Opolskie, Kujawsko Pomorskie,Lubelskie, Lubuskie, Mazowieckie✓")
print("Aktualna Wersja znajduję awarię konkretego nadajnika✓")

for i in range(1, loadbarwidth + 1):
    time.sleep(0.1)

    strbarwidth = '[{}{}] - {}\r'.format(
        (i * '✓'),
        ((loadbarwidth - i) * '-'),
        (('{:0.2f}'.format(((i) * (100/loadbarwidth))) + '% Lączenie z Google Maps'))
    )

    print(strbarwidth ,end = '')

print()
while True:

    print("Wpisz adres:")
    city = input()
    country ="PL"
    try:
        loc = geolocator.geocode(city+',' + country)
    except Exception as e:
        break
    if not loc:
        print("!!podałes bledne współrzędne!!!")
        continue

    print("Wyszukano poprawny adres!")
    time.sleep(0.5)
    print("szerokość geograficzna to :-" ,loc.latitude,"\ndlugosc geograficzna to:-" ,loc.longitude)
    time.sleep(0.5)
    print("Generowanie linku..")
    x = str(loc.latitude)
    y = str(loc.longitude)

    wspol = (x+","+y)
    url = 'http://beta.btsearch.pl/?dataSource=locations&network=26001&standards=&bands=&center='+(wspol)+'&zoom=20'

    time.sleep(1)
    print("Sukces✓")
    df = pd.read_csv('btsx.csv', dtype={'LAT': np.float64, 'LON': np.float64, 'Adres': np.str, })
    x1 = (loc.latitude)
    y1 = (loc.longitude)
    def calculateDistance(x1, y1, x2, y2):
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * 100
        return dist

    def checkIfMin(min_id, min_val, i, distances):
        if distances[-1][0] < min_val:
            min_id = i
            min_val = distances[-1][0]
        return (min_id, min_val)

    with open(f'distance.txt', encoding="utf8") as f:
        distances = []
        min_id = 0
        min_val = 999999
        for i, l in enumerate(f.read().splitlines()):
            x2, y2 = map(float, l.split(',')[:2])
            distances.append([calculateDistance(x1, y1, x2, y2), l.split('"')[1]])
            min_id, min_val = checkIfMin(min_id, min_val, i, distances)

    print("Link do Map BTS : " + url)
    print("Położenie nadajnika: %s" % distances[min_id][1])
    print("Odległość do nadajnika: %.2fKM" % distances[min_id][0])
    fopen = open('gctr.xls', mode='r+')
    fread = fopen.readlines()
    fread2 = fopen.read()
    s = substring.substringByChar(distances[min_id][1], startChar='[', endChar="]")
    bt = substring.substringByInd(s, startInd=7,  endInd=11)
    print("BT"+bt)
    warun = 0
    liniaaa = 0
    for line in fread:
        if bt in line:
            warun = warun+1
            liniaaa = line
            gctr = substring.substringByChar(liniaaa, startChar='>', endChar=".")

    if warun == 0:
      print("Brak Aktywnego GCTR")
    else:
         print("Znaleziono Aktywny GCTR : " + (gctr))
 
           
    









