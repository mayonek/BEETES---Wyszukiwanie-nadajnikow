from math import radians, cos, sin, asin, sqrt
import math
import json
from geopy.geocoders import Nominatim

import time
geolocator = Nominatim(user_agent="my-application")


transmitters = []


def calculate_distance(lon1, lat1, lon2, lat2):
  """
  Calculate the great circle distance between two points
  on the earth (specified in decimal degrees)
  """
  # convert decimal degrees to radians
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

  # haversine formula
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
  c = 2 * asin(sqrt(a))
  r = 6371  # Radius of earth in kilometers. Use 3956 for miles
  return c * r


class Transmitter:
  def __init__(self, address, distance, _ids):
    self.address = address
    self.distance = distance
    self._ids = _ids

  def print(self):
    print('<-')
    print('Address: %s' % self.address)
    print('Distance: %.3fkm' % self.distance)
    print('IDs: %s' % ', '.join(self._ids))
    print('->')


def init():
  with open('bazy/distance.json') as f:
    data = json.load(f)
  for e in data:
    distance = calculate_distance(lat1, lon1, float(e['lat']), float(e['lon']))
    transmitters.append(Transmitter(e['address'], distance, e['ids']))
    transmitters.sort(key=lambda x: x.distance)
def start():
  while True:
    print("Wpisz adres:")
    city = input()
    country = "PL"
    try:
      loc = geolocator.geocode(city + ',' + country)
    except Exception as e:
      break
    if not loc:
      print("!!podałes bledne współrzędne!!!")
      continue

    print("Wyszukano poprawny adres!")
    time.sleep(0.5)
    print("szerokość geograficzna to :-", loc.latitude, "\ndlugosc geograficzna to:-", loc.longitude)
    time.sleep(0.5)
    print("Generowanie linku..")
    x = str(loc.latitude)
    y = str(loc.longitude)

    wspol = (x + "," + y)
    url = 'http://beta.btsearch.pl/?dataSource=locations&network=26001&standards=&bands=&center=' + (wspol) + '&zoom=20'

    print("Sukces✓")
    global lat1
    lat1 = loc.latitude
    global lon1
    lon1 = loc.longitude


    break


def init():
  with open('bazy/distance.json') as f:
    data = json.load(f)
  for e in data:
    distance = calculate_distance(lat1, lon1, float(e['lat']), float(e['lon']))
    transmitters.append(Transmitter(e['address'], distance, e['ids']))
    transmitters.sort(key=lambda x: x.distance)


def loop():
  while True:
    n = int(input('How many results? '))

    for i in range(n):
      transmitters[i].print()
    break
  main()


def main():

  start()
  init()
  loop()


if __name__ == '__main__':
  main()