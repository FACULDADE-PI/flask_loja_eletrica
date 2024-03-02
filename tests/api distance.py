from requests import get
from time import sleep
import geopy.distance


def get_route_coordinates(endereco):
	params = {
		"api_key": "65d3f1849eabf972298620iga0e07c8",
		"q": endereco
	}

	r = get("https://geocode.maps.co/search", params=params)
	return r.json()[0]


def calculate_distance(coords_1:tuple, coords_2:tuple):
	return geopy.distance.geodesic(coords_1, coords_2).km




if __name__ == "__main__":
	enderecos = [{
			"endereco": "Rua Borba Gato, Bom Retiro, 123, Ipatinga, MG",
			"lon": None,
			"lat": None,
			"distance": None
		},
		{
			"endereco": "Avenida Carlos Chagas, Cidade Nobre, 531, Ipatinga, MG",
			"lon": None,
			"lat": None,
			"distance": None
		}
	]


	# for endereco in enderecos:
	# 	response = get_route_coordinates(endereco["endereco"])
	# 	endereco["lon"] = response['lon']
	# 	endereco["lat"] = response['lat']
	# 	sleep(1)


	# coords_1 = (enderecos[0]["lat"], enderecos[0]["lon"]) # aqui precisa ser a coordenada do entregador
	# coords_2 = (enderecos[-1]["lat"], enderecos[-1]["lon"])

	distance = calculate_distance((-19.5071145, -42.5521792), (-19.4662334, -42.5585013))
	print(distance)