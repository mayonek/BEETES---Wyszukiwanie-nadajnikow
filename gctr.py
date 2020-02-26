import urllib.request  as urllib2
import requests


proxy = urllib2.ProxyHandler({"http":"tmg.omnis.netia.org:8080"})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
response = urllib2.urlopen("http://10.13.194.24/DKOK/")
data = response.read() 
print(data, file=open("gctr.xls", "w"))
print(data)

http://tmg.omnis.netia.org:8080/array.dll?Get.Routing.Script