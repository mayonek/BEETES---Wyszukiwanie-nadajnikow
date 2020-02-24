from math import sin, cos, asin, atan2, sqrt, pi
import json
from geopy.geocoders import Nominatim
import time
geolocator = Nominatim(user_agent="my-application")
import substring
loadbarwidth = 10
transmitters = []
for i in range(1, loadbarwidth + 1):
    time.sleep(0.1)

    strbarwidth = '[{}{}] - {}\r'.format(
        (i * '✓'),
        ((loadbarwidth - i) * '-'),
        (('{:0.2f}'.format(((i) * (100/loadbarwidth))) + '% Lączenie z Mapami'))
    )

    print(strbarwidth ,end = '')
print("BE TE ES v2 Piotr.Wawrzyczek@netia.pl")

# def calculate_distance(lat1, lon1, lat2, lon2):
#   return geopy.distance.geodesic((lat1, lon1), (lat2, lon2)).km


# def calculate_distance(lat1, lon1, lat2, lon2):
#   return geopy.distance.vincenty((lat1, lon1), (lat2, lon2)).km

#wzór najdokładniejszy
def calculate_distance(lat1, lon1, lat2, lon2):
  p = 0.017453292519943295     #Pi/180
  a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
  return 12742 * asin(sqrt(a)) #2*R*asin...


# def rad(x):
#   return x * pi / 180


# def calculate_distance(lat1, lon1, lat2, lon2):
#   R = 6378137 # Earth’s mean radius in meter
#   d_lat = rad(lat2 - lat1)
#   d_lon = rad(lon2 - lon1)
#   a = sin(d_lat / 2) * sin(d_lat / 2) + cos(rad(lat1)) * cos(rad(lat2)) * sin(d_lon / 2) * sin(d_lon / 2)
#   c = 2 * atan2(sqrt(a), sqrt(1 - a))
#   d = R * c
#   return d / 1000 # returns the distance in kilometer

# podział bazy
class Transmitter:
  def __init__(self, address, distance, _id, network_modes):
    self.address = address
    self.distance = distance
    self._id = _id
    self.network_modes = network_modes
  #PRINTOWANIE WYNIKÓW
  def print(self):
    print('<-')
    print('Położenie BT: %s' % self.address)
    print('Dystans: %.2fkm' % self.distance)
    print('BT: %s' % self._id)
    print('Tryby sieci: %s' % ', '.join(self.network_modes))
    #print('->')
    #SZUKANIE GCTR
    gctropen = open('gctr.xls', mode='r+')
    gctrread = gctropen.readlines()
    warun = 0
    liniaaa = 0
    bts = substring.substringByInd(self._id, startInd=2, endInd=5)
    for line in gctrread:
      if  bts in line:
        warun = warun + 1
        liniaaa = line
        gctr = substring.substringByChar(liniaaa, startChar='>', endChar=".")
        gctr1 = gctr[31:]
    if warun == 0:
        print("Brak Aktywnego GCTR na "+self._id )

    else:
        print("Znaleziono Aktywny GCTR : " + (gctr1))
    return
  def to_dictionary(self):
    return {'address': self.address, 'distance': self.distance, 'id': self._id, 'network_modes': self.network_modes}


def save_to_file(n):
  save_path = 'wyniki/{}_lat_{}_lon_{}.json'.format(time.strftime("%Y-%m-%d_%Hx%M"), lat1, lon1)
  try:
    with open(save_path, 'w+') as f:
      f.write(json.dumps([t.to_dictionary() for t in transmitters[:n]], ensure_ascii=False, indent=4))
    print('Saved as %s' % save_path)
  except:
    print('Couldn\'t save the output')
def start():
  while True:
    print("Wprowadź adress:")
    city = input()
    country = "PL"
    try:
      loc = geolocator.geocode(city + ',' + country)
    except Exception as e:
      break
    if not loc:
      print("!!podałes bledne współrzędne!!!")
      continue

    print("Generowanie linku..")
    print()
    x = str(loc.latitude)
    y = str(loc.longitude)

    wspol = (x + "," + y)
    url = 'http://beta.btsearch.pl/?dataSource=locations&network=26001&standards=&bands=&center=' + (wspol) + '&zoom=20'
    print(url)

    global lat1
    lat1 = loc.latitude
    global lon1
    lon1 = loc.longitude
    break
def init():
  with open('distance.json') as f:
    data = json.load(f)
  for e in data:
    distance = calculate_distance(lat1, lon1, float(e['lat']), float(e['lon']))
    transmitters.append(Transmitter(e['address'], distance, e['id'], e['network_modes']))
  transmitters.sort(key=lambda x: x.distance)


def loop():
  # while True:
    # n = int(input('How many results? '))
  n = 3

  save_to_file(n)
  for t in transmitters[:n]:
    t.print()
  main()






def main():
  start()
  init()
  loop()


if __name__ == '__main__':
  main()