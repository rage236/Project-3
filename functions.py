from math import radians, sin, cos, sqrt, atan2
from collections import deque
import heapq

def build_graph(edges):
    graph = {}
    for edge in edges:
        if edge.source not in graph:
            graph[edge.source] = [[edge.destination, edge.distance]]
        else: 
            graph[edge.source].append([edge.destination, edge.distance])
    
    return graph

# Provided by ChatGPT
def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Radius of Earth in kilometers

    return distance

#return the vertex the closest to some lat/lon coordinate
def getClosest(gr, lat, lon):
    closest_vertex = None
    min_distance = float('inf')

    for vertex, data in gr.vertices.items():
        vertex_data = gr.get_vertex_data(vertex)
        vertex_lat, vertex_lon = vertex_data.latitude, vertex_data.longitude
        distance = haversine(lat, lon, vertex_lat, vertex_lon)

        if distance < min_distance:
            min_distance = distance
            closest_vertex = vertex

    return closest_vertex

def shortestPath_q (graph, root):
    # Initialize distances with infinity for all nodes except the start node
    distances = {node: float('inf') for node in graph}
    distances[root] = 0

    # Parent dictionary to store the parent node for each node
    parents = {node: None for node in graph}

    # Use a regular queue for BFS
    queue = deque([root])

    while queue:
        current_node = queue.popleft()

        # Explore neighbors of the current node
        for neighbor, edge_distance in graph.get(current_node, []):
            new_distance = distances[current_node] + edge_distance

            # Before updating distances, make sure the neighbor node is in the distances dictionary
            if neighbor not in distances:
                distances[neighbor] = float('inf')

            # Update the distance and parent if a shorter path is found
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                parents[neighbor] = current_node
                queue.append(neighbor)

    return distances


def shortestPath_pq(graph, root):
    # Initialize distances with infinity for all nodes except the start node
    distances = {vertex: float('infinity') for vertex in graph}
    distances[root] = 0

    priority_queue = [(0, root)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue  # Skip if a shorter path has already been found

        for neighbor, edge_distance in graph.get(current_vertex, []):
            new_distance = distances[current_vertex] + edge_distance

            if neighbor in distances and new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances

# Color Nodes based on distance from the center of downtown
def style_parent(gr, parent, data, max_distance):
    colors = ['red', 'orangered', 'tomato', 'orange', 'gold', 'yellow', 'greenyellow', 'mediumspringgreen', 'cyan', 'dodgerblue', 'blue', 'darkblue', 'indigo', 'purple', 'magenta', 'deeppink', 'pink', 'lightpink', 'white']
    if data != float('inf'):
        gr.get_vertex(parent).color = colors[min(int(data/max_distance * len(colors)), len(colors) - 1)]
    else:
        gr.get_vertex(parent).color = "black"
