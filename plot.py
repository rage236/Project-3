from bridges.data_src_dependent import data_source
from cities import cities
import time
from functions import *
import matplotlib.pyplot as plt

def plot():
    vertices_list = []
    pq_times = []
    q_times = []

    iterations = int(input("# of iterations?" + '\n'))
    
    for city in cities:
        osm_data = data_source.get_osm_data(city, "default")
        gr = osm_data.get_graph()

        root = getClosest(gr,
                        (osm_data.latitude_range[0]+osm_data.latitude_range[1])/2,
                        (osm_data.longitude_range[0]+osm_data.longitude_range[1])/2)
        
        g = build_graph(osm_data.edges) 

        vertices = len(g)
        vertices_list.append(vertices)


        # Priority Queue
        start = time.time()
        for i in range(iterations):
            shortestPath_pq(g, root)
        end = time.time()
        pq_times.append((end - start) / iterations)

        # Regular Queue
        start = time.time()
        for i in range(iterations):
            shortestPath_q(g, root)
        end = time.time()
        q_times.append((end - start) / iterations)

    # Plotting
    plt.scatter(vertices_list, pq_times, label='Priority Queue', marker='o')
    plt.scatter(vertices_list, q_times, label='Queue', marker='x')
    plt.xlabel('Number of Vertices')
    plt.ylabel('Time (seconds)')
    plt.title('Shortest Path Algorithm Performance')
    plt.legend()
    plt.show()