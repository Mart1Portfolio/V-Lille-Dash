#In this python script we use the geopy library to convert an address to coordinates and vice versa.
#We have 3 functions:
#1. address_to_coordinates(address) - converts an address to coordinates
#2. coordinates_to_address(coordinates) - converts coordinates to an address
#3. calculate_distance(coordinates1, coordinates2) - calculates the distance between two coordinates


# The documentation for the geopy library can be found at https://geopy.readthedocs.io/en/latest/

def address_to_coordinates(address : str) -> tuple:
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="V_Lille_App")
    location = geolocator.geocode(address)
    return (location.latitude, location.longitude)




def coordinates_to_address(coordinates : tuple) -> str:
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="V_Lille_App")
    location = geolocator.reverse(coordinates)
    return location.address

def calculate_distance(coordinates1 : tuple, coordinates2 : tuple) -> float:
    from geopy.distance import geodesic
    return geodesic(coordinates1, coordinates2).kilometers