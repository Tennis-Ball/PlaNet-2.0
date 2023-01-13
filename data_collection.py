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
