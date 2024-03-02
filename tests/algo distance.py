from geopy.geocoders import Nominatim
import osmnx as ox
import networkx as nx

def metros_para_km(distancia_metros):
    distancia_km = distancia_metros / 1000.0
    return distancia_km

def obter_grafo_estradas(coordenadas, distancia_metros=500):
    point = ox.utils.geocode(coordenadas)
    G = ox.graph_from_point(point, distance=distancia_metros, network_type='walk')
    return G

def calcular_distancia_entre_pontos(coordenadas_origem, coordenadas_destino, grafo_estradas):
    origem = ox.distance.nearest_nodes(grafo_estradas, *ox.utils.geocode(coordenadas_origem))
    destino = ox.distance.nearest_nodes(grafo_estradas, *ox.utils.geocode(coordenadas_destino))
    
    rota = nx.shortest_path(grafo_estradas, origem, destino, weight='length')
    distancia = sum(ox.utils_graph.get_route_edge_attributes(grafo_estradas, rota, 'length'))
    
    return distancia

# Exemplo de uso
coordenadas_origem = "Rua Borba Gato, Bom Retiro, Ipatinga"
coordenadas_destino = "Rua Carlos Chagas, Cidade Nobre, Ipatinga"

grafo_estradas = obter_grafo_estradas(coordenadas_origem)
distancia_em_metros = calcular_distancia_entre_pontos(coordenadas_origem, coordenadas_destino, grafo_estradas)
distancia_em_km = metros_para_km(distancia_em_metros)

print(f"A distância entre os pontos é de {distancia_em_km:.2f} km.")
print(f"A distância entre os pontos é de {distancia_em_metros:.2f} metros.")