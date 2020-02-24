import math
from geopy.geocoders import Nominatim
import substring
import time
print("Wpisz adres:")
city = input()
geolocator = Nominatim(user_agent="my-application")
loadbarwidth = 23
country = "PL"
    try:
        loc = geolocator.geocode(city + ',' + country)
    except Exception as e:
        break
    if not loc:
        print("!!podałes bledne współrzędne!!!")
        continue


def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * 100
    return dist


with open(f'distance.txt', encoding="utf8", errors='ignore') as f:
      distances = []
      for i, l in enumerate(f.read().splitlines()):
        x2, y2 = map(float, l.split(',')[:2])
        distances.append([calculateDistance(x1, y1, x2, y2), l.split('"')[1]])
      distances.sort(key=lambda x: x[0])
      n = int(input("How many results? "))
      for e in distances[:n]:
        print("Nadajnik: {} | Odległość od nadajnika: {}".format(e[1], round(e[0], 2)))
