from bridges.data_src_dependent import data_source
from bridges.bridges import Bridges
from cities import cities, city_prompt
from functions import *
import plot

def main():
    bridges = Bridges(209, "PKromash", "930462735290")

    bridges.set_title("Graph : OpenStreet Map Example")
    bridges.set_description("OpenStreet Map data of various cities, with colors based on distance from the center of downtown")

    city = -1
    while city < 1 or city > 34:
        city = input(city_prompt)
        if city == "plot":
            plot.plot()
            return
        city = int(city)

    osm_data = data_source.get_osm_data(cities[city - 1], "default")

    gr = osm_data.get_graph()
    gr.force_large_visualization(True)

    # Get the center of the city
    root = getClosest(gr,
                         (osm_data.latitude_range[0]+osm_data.latitude_range[1])/2,
                         (osm_data.longitude_range[0]+osm_data.longitude_range[1])/2)

    g = build_graph(osm_data.edges)

    distance = shortestPath_pq(g, root)

    max_distance = -1
    for vertex, data in distance.items():
        if data != float('inf') and data > max_distance:
            max_distance = data
        
    for vertex, data in distance.items():
        style_parent(gr, vertex, data, max_distance)

    bridges.set_data_structure(gr)
    bridges.visualize()

if __name__ == "__main__":
    main()
