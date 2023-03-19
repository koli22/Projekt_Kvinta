import networkx as nx
import itertools

def find_optimal_path(stations, paths, vehicles):
    """
    Find the optimal path for multiple vehicles given the stations and paths.

    Parameters:
    stations (list of tuples): A list of tuples representing the stations. Each tuple contains the station ID and its capacity.
    paths (list of tuples): A list of tuples representing the paths. Each tuple contains the path ID, its capacity, its length, and the IDs of the start and end stations.
    vehicles (list of tuples): A list of tuples representing the vehicles. Each tuple contains the vehicle ID, the ID of its starting station, and the ID of its ending station.

    Returns:
    A dictionary mapping each vehicle ID to its optimal path, represented as a list of path IDs.
    """
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes for the stations
    for station in stations:
        G.add_node(station[0], demand=-station[1])

    # Add nodes and edges for the paths
    for path in paths:
        G.add_node(path[0], demand=path[1])
        G.add_edge(path[3], path[0], weight=path[2])
        G.add_edge(path[0], path[4], weight=0)

    # Find all permutations of the vehicles
    vehicle_permutations = list(itertools.permutations(vehicles))

    # Initialize the optimal path dictionary
    optimal_paths = {}

    # Loop through all permutations of the vehicles
    for vehicle_order in vehicle_permutations:
        # Initialize the flow dictionary
        flow_dict = {}

        # Loop through the vehicles in the current order
        for vehicle in vehicle_order:
            # Add a node for the vehicle
            G.add_node(vehicle[0], demand=1)

            # Add edges for the starting and ending stations of the vehicle
            G.add_edge(vehicle[0], vehicle[1], weight=0)
            G.add_edge(vehicle[0], vehicle[2], weight=0)

            # Add the vehicle to the flow dictionary
            flow_dict[(vehicle[0], vehicle[1])] = 1
            flow_dict[(vehicle[0], vehicle[2])] = -1

        # Calculate the minimum cost flow
        flow_cost, flow_dict = nx.network_simplex(G, demand='demand', capacity='capacity', weight='weight', flow_func=nx.min_cost_flow)

        # If this is the first iteration or if the current solution is better than the previous one
        if not optimal_paths or flow_cost < min(optimal_paths.keys()):
            # Update the optimal path dictionary with the current solution
            optimal_paths = {}

            for vehicle in vehicle_order:
                path = []
                node = vehicle[1]

                while node != vehicle[2]:
                    for edge in G.edges(node, data=True):
                        if edge[2]['flow'] == 1 and edge[1] != vehicle[2]:
                            path.append(edge[2]['id'])
                            node = edge[1]

                optimal_paths[vehicle[0]] = path

    return optimal_paths





# Define the stations and paths
stations = [('A', 1), ('B', 1), ('C', 1), ('D', 1)]
paths = [('P1', 1, 5, 'A', 'B'),
         ('P2', 1, 3, 'B', 'C'),
         ('P3', 1, 2, 'C', 'D'),
         ('P4', 1, 6, 'A', 'C'),
         ('P5', 1, 4, 'B', 'D')]

# Define the vehicles
vehicles = [('V1', 'A', 'D'),
            ('V2', 'B', 'C'),
            ('V3', 'C', 'A')]

# Find the optimal path for each vehicle
optimal_paths = find_optimal_path(stations, paths, vehicles)

# Print the optimal paths for each vehicle
for vehicle_id, path in optimal_paths.items():
    print(f"Vehicle {vehicle_id}: {path}")
