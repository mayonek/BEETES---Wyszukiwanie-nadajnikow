from math import sin, cos, asin, atan2, sqrt, pi
import json
import time
from geopy.geocoders import Nominatim
import substring
import ftplib
geolocator = Nominatim(user_agent="my-application")
def calculate_distance(lat1, lon1, lat2, lon2):
  p = 0.017453292519943295 #Pi/180
  a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
  return 12742 * asin(sqrt(a)) #2*R*asin...
print("BETEES - piotr.wawrzyczek@netia.pl")



def pobierzgctr():

  path = '/'
  filename = 'gctr2.html'

  ftp = ftplib.FTP("serwer1987047.home.pl") 
  ftp.login("admin@momail.site", "Jamnik22!") 
  ftp.cwd(path)
  ftp.retrbinary("RETR " + filename, open(filename, 'wb').write)
  ftp.quit()
  
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    orange='\033[33m'
class Transmitter:
  def __init__(self, address, lat, lon, distance, _id, network_modes):
    self.address = address
    self.lat = lat
    self.lon = lon
    self.distance = distance
    self._id = _id
    self.network_modes = network_modes

  def print(self):
    if self.distance > 5:
      print(f"{bcolors.FAIL}"' ')
    if self.distance < 5:
      print(f"{bcolors.OKGREEN}"' ')
    if self.distance > 3 and self.distance < 5:
      print(f"{bcolors.orange}"' ')
    
    print('Adres: %s' % self.address)
    print('Dystans: %.2fkm' % self.distance)
    print('Id: %s' % self._id)
    print('Tryby sieci: %s' % ', '.join(self.network_modes))
        # print('->')
        # SZUKANIE GCTR
    
    gctropen = open('gctr2.html', mode='r+')
    
    gctrread = gctropen.readlines()
    warun = 0
    liniaaa = 0
    bts = substring.substringByInd(self._id, startInd=2, endInd=6)
    for line in gctrread:
        if bts in line:
            warun = warun + 1
            liniaaa = line
            gctr = substring.substringByChar(liniaaa, startChar='>', endChar="</td>")
            gctr1 = gctr[27:]
    if warun == 0:
       print("Brak Aktywnego GCTR na :" + self._id)
       
    else:
       print(f"{bcolors.FAIL}Znaleziono Aktywny GCTR :  " + (gctr1))

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
    pobierzgctr()
    global city
    city = input(f"{bcolors.BOLD}Wprowadź miasto:{bcolors.ENDC}")
    global ul
    ul = input(f"{bcolors.BOLD}Wprowadź ulice:{bcolors.ENDC}")
    country = 'PL'

    try:
      loc = geolocator.geocode(ul + "," + city + ',' + country)
    except Exception as e:
      print(e)
      break
    if not loc:
      print('Podane współrzędne są błędne')
      continue

    return (loc.latitude, loc.longitude)


def generate_link(lat1, lon1):
  print('')
  print('Wyszukiwany adres : '+ city  + " " + ul)
  
  url = 'http://beta.btsearch.pl/?dataSource=locations&network=26001&standards=&bands=&center={},{}&zoom=20'.format(lat1, lon1)
  
  print('')
  print("Link do map btsearch")
  print(f"{bcolors.OKBLUE}"+f"{bcolors.BOLD}"+url+bcolors.ENDC)
  
  


def init(lat1, lon1, transmitters):
  with open('distance.json', encoding="windows-1250") as f:
    data = json.load(f)
  for e in data:
    lat2 = float(e['lat'])
    lon2 = float(e['lon'])
    transmitters.append(Transmitter(e['address'], lat2, lon2, 0, e['id'], e['network_modes']))
def leftgctr():
  gctropen = open('gctr2.html', mode='r+')

  gctrread = gctropen.readlines()
  warun = 0
  liniaaa = 0
  city1 = city.upper()

  for line in gctrread:
    if city1 in line:
      liniaaa = line
      #gctr = substring.substringByChar(liniaaa, startChar='>', endChar="</td>")
      gctr1 = liniaaa[43:]
      print(f"{bcolors.FAIL}GCTRy aktywne w mieście " + city1 + " sprawdź http://10.13.194.24/DKOK/")
      print(" ")
      print(gctr1)
      break
def dodatki(lat1, lon1):
  
  print("Dodatkowe narzędzia:↓")
  print("Link do mapy ukształtowania terenu ↓")
  urlgoogle = 'https://www.google.com/maps/@{},{},245a,35y,39.15t/data=!3m1!1e3'.format(lat1, lon1)
  urlplus = 'https://www.plus.pl/mapa-zasiegu'
  print(f"{bcolors.OKBLUE}"+f"{bcolors.BOLD}"+urlgoogle+bcolors.ENDC)
  print('')
  print("Sprawdź pokrycie zasięgowe ↓ ")
  print(f"{bcolors.OKBLUE}"+f"{bcolors.BOLD}"+urlplus+bcolors.ENDC)
  
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
    
    leftgctr()
    dodatki(lat1, lon1)
if __name__ == '__main__':
  main()