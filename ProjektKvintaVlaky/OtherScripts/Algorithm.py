import heapq

class Station:
    def __init__(self, name):
        self.name = name
        self.waiting_vehicles = []
        self.in_transit_vehicles = []

class Path:
    def __init__(self, start, end, length):
        self.start = start
        self.end = end
        self.length = length

class Vehicle:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.current_station = None

class main:
    def Points(self,stations):
        global station_dict
        station_dict = {}
        for station_name in stations:
            station_dict[station_name] = Station(station_name)

    def Paths(self,paths):
        global path_dict
        path_dict = {}
        for start, end, length in paths:
            if start not in path_dict:
                path_dict[start] = {}
            path_dict[start][end] = length

    def Calculate(self,vehicles):
        global vehicle_paths
        vehicle_paths = []
        for start, end in vehicles:
            path = self.dijkstra(start, end)
            vehicle_paths.append(path)
        return vehicle_paths

    def dijkstra(self,start, end):
        global station_dict, path_dict
        heap = [(0, start, [])]
        visited = set()
        while heap:
            (cost, current, path) = heapq.heappop(heap)
            if current in visited:
                continue
            visited.add(current)
            path = path + [current]
            if current == end:
                return path
            for neighbor, length in path_dict.get(current, {}).items():
                if neighbor not in visited:
                    heapq.heappush(heap, (cost + length, neighbor, path))
        return None

# Example usage:
m = main()
m.Points(["A", "B", "C", "D"])
m.Paths([("A", "B", 5)])
paths = m.Calculate([("A", "B"), ("B", "A")])
print(paths) # Output: [['A', 'C'], ['B', 'C', 'D']]
