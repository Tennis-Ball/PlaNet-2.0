# Aggregates images from around world with corresponding location information
# including continent, country, and (state?) city
# Place id to location: https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJrTLr-GyuEmsRBfy61i59si0&key=APIKEY
# Coords to road coors: https://roads.googleapis.com/v1/snapToRoads?interpolate=true&path=-35.284728747199374%2C149.12834860726772%7C-35.28032%2C149.12907%7C-35.28099%2C149.12929%7C-35.28144%2C149.12984%7C-35.28194%2C149.13003%7C-35.28282%2C149.12956%7C-35.28302%2C149.12881%7C-35.28473%2C149.12836&key=APIKEY
# Coords to image: https://maps.googleapis.com/maps/api/streetview?size=600x300&location=-35.2784195,149.12946589999999&heading=120&key=APIKEY
# Download online image: https://stackoverflow.com/questions/30229231/python-save-image-from-url

# New plan: use selenium to open maps browser, go into streetview, press forward and capture
# coordinates from url. When a dead end is encountered rotate 90 degrees and continue.
# If coordinates have already been seen, ignore them.
# Once a land mass is sufficiently covered, start at a new one
# Deploy in an ec2 instance for continuous running
# Multithreading??
import requests
import json


with open("maps_api_key.txt", "r") as key:
    API_KEY = key.read().strip()
key.close()

class Break_continue(Exception):
    pass
break_continue = Break_continue()

init_lat = 42.397
init_long = -71.186  # top left rectilinear area
end_lat = 42.234
end_long = -71.008
int_height = int(init_lat*1000 - end_lat*1000)
int_width = int(end_long*1000 - init_long*1000)
print("Max images:", int_height*int_width)

coords = set()

for shift_vert in range(int_height):
    for shift_horiz in range(int_width):
        neighborhood = None
        lat = init_lat - shift_vert/1000
        long = init_long + shift_horiz/1000
        # get progress
        if shift_horiz%100==0:
            print(f"{shift_horiz/int_width}% x {shift_vert/int_height}%")

        # get location information
        r = requests.get(f"https://roads.googleapis.com/v1/snapToRoads?interpolate=true&path={lat},{long}&key={API_KEY}").content
        try:
            json_info = json.loads(r)["snappedPoints"][0]
            place_id = json_info["placeId"]
        except KeyError:
            continue
        SV_lat = json_info["location"]["latitude"]
        SV_long = json_info["location"]["longitude"]

        # get geographical information
        r = requests.get(f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={API_KEY}").content
        try:
            for component in json.loads(r)["result"]["address_components"]:
                if "neighborhood" in component["types"]:
                    neighborhood = component["long_name"]
                elif "locality" in component["types"] and component["long_name"] != "Boston":
                    raise break_continue
                elif "country" in component["types"] and neighborhood != None:
                    break
        except (KeyError, Break_continue):
            continue

        # get streetview images
        for rot in range(4):  # 360 degree images
            img_data = requests.get(f"https://maps.googleapis.com/maps/api/streetview?size=180x90&location={SV_lat},{SV_long}&heading={str(90*rot)}&key={API_KEY}").content
            with open(f"images_data/{str(shift_vert*int_width+shift_horiz)}({str(rot+1)}).jpg", "wb") as handler:
                handler.write(img_data)
            handler.close()

        coords.add((str(shift_vert*int_width+shift_horiz), neighborhood))

print(len(coords))
with open("coords.txt", "w") as f:
    f.write(str(coords))
f.close()
