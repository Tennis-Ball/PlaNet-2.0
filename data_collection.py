# Aggregates images from around world with corresponding location information
# including continent, country, and (state?) city
# Place id to location: https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJrTLr-GyuEmsRBfy61i59si0&key=APIKEY
# Coords to road coors: https://roads.googleapis.com/v1/snapToRoads?interpolate=true&path=-35.284728747199374%2C149.12834860726772%7C-35.28032%2C149.12907%7C-35.28099%2C149.12929%7C-35.28144%2C149.12984%7C-35.28194%2C149.13003%7C-35.28282%2C149.12956%7C-35.28302%2C149.12881%7C-35.28473%2C149.12836&key=APIKEY
# Coords to image: https://maps.googleapis.com/maps/api/streetview?size=600x300&location=-35.2784195,149.12946589999999&heading=120&key=APIKEY
# Download online image: https://stackoverflow.com/questions/30229231/python-save-image-from-url

import requests
import re


def extract_coords(json_string):
    segment = json_string[json_string.find("latitude")+11:]
    latitude = segment[:segment.find(",")]
    longitude = segment[segment.find("longitude")+12:segment.find("\n      }")]
    return latitude, longitude


def get_data(type):
    image_url = "test url"
    img_data = requests.get(image_url).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)

    # type is the level of geographical specificity: continent, country, or state/city
    images = []  # RGB pixel matrix
    labels = []  # Label strings to be converted to scalars
    return images, labels

lat, long = "-35.284728747199374", "149.12834860726772"
lat, long = "42.3436709", "-71.0768575"
seen = [(lat, long)]
json_string = requests.get(f"https://roads.googleapis.com/v1/snapToRoads?interpolate=true&path={lat}%2C{long}&key=APIKEY").text
lat, long = extract_coords(json_string)

while (lat, long) not in seen:
    seen.append((lat, long))
    json_string = requests.get(f"https://roads.googleapis.com/v1/snapToRoads?interpolate=true&path={lat}%2C{long}&key=APIKEY").text
    print(json_string)
    lat, long = extract_coords(json_string)
    print(len(seen))

print((lat, long))
print(seen)

for i in range(7**24):
    if i % (1000000000000000) == 0:
        print(i)

print("done")
