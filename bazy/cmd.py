from geopy.geocoders import GoogleV3
google_key = "AIzaSyCYXmN6XNbZCziryf0LjTXilQq4MMPB7dY"
g = GoogleV3(api_key=google_key)
print("ADRES?!")

locations = g.geocode(components={"city": "Paris", "country": "FR"})
geocode_result = g.geocode(locations)

print(geocode_result)  # select first location
