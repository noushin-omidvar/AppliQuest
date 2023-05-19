import requests


def get_map_html(center, zoom, width, height, access_token):
    mapbox_url = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/{lon},{lat},{zoom},0,0/{width}x{height}?access_token={access_token}"
    map_url = mapbox_url.format(lon=center.split(",")[0], lat=center.split(
        ",")[1], zoom=zoom, width=width, height=height, access_token=access_token)
    return f'<iframe src="{map_url}" width="{width}" height="{height}" frameborder="0"></iframe>'


def get_markers(cities, access_token):
    markers = []
    for city in cities:
        geocode_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{city['address']}.json?access_token={access_token}"
        response = requests.get(geocode_url)
        data = response.json()
        marker = {
            "name": city["name"],
            "lng": data["features"][0]["center"][0],
            "lat": data["features"][0]["center"][1]
        }
        markers.append(marker)
    return markers
