from  geopy.geocoders import Nominatim
import webbrowser
import time
import pandas as pd
import numpy as np
geolocator = Nominatim(user_agent="my-application")
loadbarwidth = 23
print("################################################")
print("BE TE ESIK v0.01 by Pan! Piotr Wawrzyczek")
print("------------------------------------------------------------------")
print("Podaj Adres w następującej kolejności:")

print("program pokaże dokładany adres na środku ekranu")
for i in range(1, loadbarwidth + 1):
    time.sleep(0.2)

    strbarwidth = '[{}{}] - {}\r'.format(
        (i * '@'),
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
    print("Otwieranie BTS")
    x = str(loc.latitude)
    y = str(loc.longitude)

    wspol = (x+","+y)
    url = 'http://beta.btsearch.pl/?dataSource=locations&network=26001&standards=&bands=&center='+(wspol)+'&zoom=20'
    webbrowser.open(url, new=2)
    time.sleep(1)
    print("Sukces")
    df = pd.read_csv('btsx.csv', dtype={'LAT': np.float64, 'LON': np.float64, 'Adres': np.str, })
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
    K = loc.latitude
    K2 = loc.longitude
    x2 = (closest(lst, K))
    y2 = (closest(lst2, K2))

    x1 = (loc.latitude)
    y1 = (loc.longitude)



    def calculateDistance(x1, y1, x2, y2):
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * 100
        return dist






