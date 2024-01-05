from dataclasses import dataclass
from enum import Enum
from math import sin, acos, cos
from pprint import pp
from typing import Optional

import faker
import folium
import osmnx as ox
from folium.features import DivIcon
from geopy.geocoders import Nominatim
from haversine import haversine

FAKE = faker.Faker()


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    GRAY = "gray"
    ORANGE = "orange"
    BEIGE = "beige"
    PINK = "pink"
    VIOLET = "violet"
    PURPLE = "purple"
    CADETBLUE = "cadetblue"
    BROWN = "brown"
    BLACK = "black"

    @classmethod
    def get_colors(cls):
        for color in list(cls):
            yield color.value


@dataclass
class Place:
    lat: float
    lon: float
    name: str
    to_destination: Optional[float] = None

    def get_position(self):
        return (self.lat, self.lon)


def get_metadata(*args):
    geolocator = Nominatim(user_agent=FAKE.user_agent())
    places = []
    for arg in args:
        location = geolocator.geocode(arg)
        places.append(Place(lat=location.latitude, lon=location.longitude, name=arg))
    return places


def main():
    start_pos = get_metadata("Kielce")[0]
    names = {
        "Oksza",
        "Rzeszów",
        "Radom",
        "Krzyżanowice",
        "Bielsko-Biała",
        "Siedlce",
        "Wtórek",
        "Izbica Kujawska",
        "Opole",
        "Biała Wieś",
        "Wilga",
        "Gwiździny",
    }

    places = get_metadata(*names)
    for place in places:
        place.to_destination = haversine(place.get_position(), start_pos.get_position(), unit="km")

    fg = folium.FeatureGroup(name="Trasa Disco Polo")
    m = folium.Map(start_pos.get_position(), zoom_start=8)

    color_gen = Color.get_colors()
    for place in places:
        info = f"<h5><b>{place.name}</b></h5><h6><b>{place.to_destination:.2f}</b></h6>"
        marker = folium.CircleMarker(
            location=place.get_position(),
            tooltip=info,
            popup=folium.Popup(info, show=True),
            fill_color=next(color_gen),
            fill=True,
            color=False,
            opacity=0,
            fill_opacity=1,
            radius=20,
        )
        fg.add_child(marker)

    m.add_child(fg)
    m.save("route.html")


if __name__ == "__main__":
    main()