from  geopy.geocoders import Nominatim
import substring
import time
import pandas as pd
import numpy as np
import math
import webbrowser
# Śląsk,Dolnyślask,Małopolska,Opolskie
geolocator = Nominatim(user_agent="my-application")
loadbarwidth = 23
print("################################################")
print("BETEES v1.01 by piotr.wawrzyczek@netia.pl")
print("Wszystkie nadajnik dodane")
print("Aktualna Wersja znajduję awarię konkretego nadajnika✓")

for i in range(1, loadbarwidth + 1):
    time.sleep(0.1)

    strbarwidth = '[{}{}] - {}\r'.format(
        (i * '✓'),
        ((loadbarwidth - i) * '-'),
        (('{:0.2f}'.format(((i) * (100/loadbarwidth))) + '% Lączenie z Mapami'))
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

    with open(f'distance.txt') as f:
      distances = []
      min_id = 0
      min_val = 999999
      for i, l in enumerate(f.read().splitlines()):
        x2, y2 = map(float, l.split(',')[:2])
        distances.append([calculateDistance(x1, y1, x2, y2), l.split('"')[1]])
        min_id, min_val = checkIfMin(min_id, min_val, i, distances)
      n = int(input("Ile nadajników? "))
      results = distances[:n]
      results.sort(key=lambda x: x[0])
      
    
    print("Link do Map BTS : " + url)
    print("Adres klineta : " +city)
    print("Nadajnik: %s" % distances[min_id][1])
    print("Odległość do nadajnika: %.2fKM" % distances[min_id][0])
    ad = substring.substringByChar(distances[min_id][1], startChar='[', endChar="]")
    bts = substring.substringByInd(ad, startInd=7,  endInd=11)
    gopen = open('distance.txt', mode='r+')
    gread = gopen.readlines()
    # Po numerze BT szuka w linii trybu pracy 
    for line in gread:
       if bts in line:
        line1 = substring.substringByChar(line, startChar='[', endChar="]")
        if "G900" in line1:
          continue
        if "U2100" in line1:     
          continue
        if "L1800" in line1:  
          continue
        else:
          print("Tryby sieci : 2G/3G/LTE")
          break
        
       
        
    a = distances[min_id][0]
    b = 5
    
    fopen = open('gctr.xls', mode='r+')
    fread = fopen.readlines()
    fread2 = fopen.read()
    s = substring.substringByChar(distances[min_id][1], startChar='[', endChar="]")
    bt = substring.substringByInd(s, startInd=7,  endInd=11)
    warun = 0
    liniaaa = 0
    for line in fread:
        if bt in line:
            warun = warun+1
            liniaaa = line
            gctr = substring.substringByChar(liniaaa, startChar='>', endChar=".")
            gctr1 = gctr[31:]
    if warun == 0:
      print("Brak Aktywnego GCTR")
    else:
         print("Znaleziono Aktywny GCTR : " + (gctr1))
    if a >= b:
      print("Prawdopodbnie BMT")
           
    









