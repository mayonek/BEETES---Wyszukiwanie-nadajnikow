from math import sin, cos, asin, atan2, sqrt, pi
import json
import time
from geopy.geocoders import Nominatim
import substring
geolocator = Nominatim(user_agent="my-application")
def calculate_distance(lat1, lon1, lat2, lon2):
  p = 0.017453292519943295 #Pi/180
  a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
  return 12742 * asin(sqrt(a)) #2*R*asin...


class Transmitter:
  def __init__(self, address, lat, lon, distance, _id, network_modes):
    self.address = address
    self.lat = lat
    self.lon = lon
    self.distance = distance
    self._id = _id
    self.network_modes = network_modes

  def print(self):
    print('<-')
    print('Adres: %s' % self.address)
    print('Dystans: %.3fkm' % self.distance)
    print('Id: %s' % self._id)
    print('Tryby sieci: %s' % ', '.join(self.network_modes))
        # print('->')
        # SZUKANIE GCTR
    gctropen = open('gctr.xls', mode='r+')
    gctrread = gctropen.readlines()
    warun = 0
    liniaaa = 0
    bts = substring.substringByInd(self._id, startInd=2, endInd=6)
    for line in gctrread:
        if bts in line:
            warun = warun + 1
            liniaaa = line
            gctr = substring.substringByChar(liniaaa, startChar='>', endChar=".")
            gctr1 = gctr[31:]
    if warun == 0:
       print("Brak Aktywnego GCTR na " + self._id)

    else:
       print("Znaleziono Aktywny GCTR : " + (gctr1))

  def to_dictionary(self):
    return {'address': self.address, 'lat': self.lat, 'lon': self.lon, 'distance': self.distance, 'id': self._id, 'network_modes': self.network_modes}


def save_to_file(lat1, lon1, transmitters, n):
  save_path = 'wynik/{}_lat_{}_lon_{}.json'.format(time.strftime("%Y-%m-%d_%H-%M"), lat1, lon1)
  try:
    with open(save_path, 'w+') as f:
      f.write(json.dumps([t.to_dictionary() for t in transmitters[:n]], ensure_ascii=False, indent=4))
    print('Zapisano jako %s\n' % save_path)
  except:
    print(' ')


def update_distances(lat1, lon1, transmitters):
  for t in transmitters:
    t.distance = calculate_distance(lat1, lon1, t.lat, t.lon)
  transmitters.sort(key=lambda x: x.distance)


def get_lat_lon(geolocator):
  while True:
    city = input('Wprowadź adres: ')
    country = 'PL'

    try:
      loc = geolocator.geocode(city + ',' + country)
    except Exception as e:
      print(e)
      break
    if not loc:
      print('Podane współrzędne są błędne')
      continue

    return (loc.latitude, loc.longitude)


def generate_link(lat1, lon1):
  print('Generowanie linku')
  url = 'http://beta.btsearch.pl/?dataSource=locations&network=26001&standards=&bands=&center={},{}&zoom=20'.format(lat1, lon1)
  print(url)


def init(lat1, lon1, transmitters):
  with open('distance.json', encoding="windows-1250") as f:
    data = json.load(f)
  for e in data:
    lat2 = float(e['lat'])
    lon2 = float(e['lon'])
    transmitters.append(Transmitter(e['address'], lat2, lon2, 0, e['id'], e['network_modes']))


def main():
  lat1 = 50.385550
  lon1 = 18.902662
  transmitters = []
  n = 3
  
  geolocator = Nominatim(user_agent="my-application")
  init(lat1, lon1, transmitters)
  while True:
    lat1, lon1 = get_lat_lon(geolocator)
    generate_link(lat1, lon1)
    update_distances(lat1, lon1, transmitters)
    for t in transmitters[:n]:
      t.print()
    save_to_file(lat1, lon1, transmitters, n)


if __name__ == '__main__':
  main()