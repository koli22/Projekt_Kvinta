#include <iostream>
#include <unordered_map>
#include <queue>
#include <vector>
#include <tuple>
#include <limits>
#include <chrono>
using namespace std;

// Create a struct to store the station information
struct Station {
    string name;
    int capacity;
    priority_queue<int, vector<int>, greater<int>> departure_times;

    Station(string name, int capacity) : name(name), capacity(capacity) {}
};

// Create a struct to store the path information
struct Path {
    string start;
    string end;
    int length;

    Path(string start, string end, int length) : start(start), end(end), length(length) {}
};

// Function to add stations
void Points(vector<Station>& stations, vector<string> station_names) {
    for (string name : station_names) {
        Station station(name, 1);
        stations.push_back(station);
    }
}

// Function to add paths between stations
void Paths(vector<Path>& paths, vector<tuple<string, string, int>> path_tuples) {
    for (auto path_tuple : path_tuples) {
        string start = get<0>(path_tuple);
        string end = get<1>(path_tuple);
        int length = get<2>(path_tuple);
        Path path(start, end, length);
        paths.push_back(path);
    }
}

// Function to calculate the optimal path for each vehicle
vector<tuple<pair<string, string>, vector<string>, int>> Calculate(vector<Path>& paths, vector<Station>& stations, vector<pair<string, string>> vehicles) {
    // Create a map to store the stations and their paths
    unordered_map<string, unordered_map<string, int>> station_paths;
    for (Path path : paths) {
        station_paths[path.start][path.end] = path.length;
    }

    vector<tuple<pair<string, string>, vector<string>, int>> optimal_paths;

    for (auto vehicle : vehicles) {
        string start = vehicle.first;
        string end = vehicle.second;

        // Create a priority queue to store the possible paths
        priority_queue<tuple<int, int, string, vector<string>>, vector<tuple<int, int, string, vector<string>>>, greater<tuple<int, int, string, vector<string>>>> pq;

        // Add the starting station to the queue
        vector<string> initial_path = {start};
        pq.push(make_tuple(0, 0, start, initial_path));

        // Create a set to store the visited stations
        unordered_map<string, int> visited_stations;

        // Initialize the departure time to 0
        int departure_time = 0;

        // Continue until all possible paths have been explored
        while (!pq.empty()) {
            auto current_state = pq.top();
            pq.pop();

            int current_time = get<0>(current_state);
            int waiting_time = get<1>(current_state);
            string current_station = get<2>(current_state);
            vector<string> current_path = get<3>(current_state);

            // Check if the current station is the destination
            if (current_station == end) {
                optimal_paths.push_back(make_tuple(vehicle, current_path, current_time));
                break;
            }

            // Check if the current station has been visited before
            if (visited_stations.find(current_station) != visited_stations.end() && visited_stations[current_station] <= current_time) {
                continue;
            }

            // Mark the current station as visited
            visited_stations[current_station] = current_time;

            // Check if the current station has capacity for the vehicle
            Station& station = stations[find_if(stations.begin(), stations.end(), [&](const Station& s) { return s.name == current_station; }) - stations.begin()];
            if (station.departure_times.size() >= station.capacity) {
                // Calculate the waiting time for the next available departure
                int next_departure_time = station.departure_times.top();
                int new_waiting_time = next_departure_time - current_time;

                // Check if waiting at the station is possible
                if (new_waiting_time > 0) {
                    // Add the waiting time to the current time
                    current_time += new_waiting_time;
                }
            }

            // Calculate the possible paths from the current station
            for (auto path : station_paths[current_station]) {
                string next_station = path.first;
                int travel_time = path.second;

                // Check if the next station has been visited before
                if (visited_stations.find(next_station) != visited_stations.end() && visited_stations[next_station] <= current_time + travel_time) {
                    continue;
                }

                // Calculate the next departure time from the current station
                int next_departure_time = current_time + travel_time;

                // Check if the next station has capacity for the vehicle
                Station& next_station_obj = stations[find_if(stations.begin(), stations.end(), [&](const Station& s) { return s.name == next_station; }) - stations.begin()];
                if (next_station_obj.departure_times.size() >= next_station_obj.capacity) {
                    // Calculate the waiting time for the next available departure
                    int next_available_departure_time = next_station_obj.departure_times.top();
                    int new_waiting_time = next_available_departure_time - next_departure_time;

                    // Check if waiting at the station is possible
                    if (new_waiting_time > 0) {
                        // Add the waiting time to the next departure time
                        next_departure_time += new_waiting_time;
                    }
                }

                // Add the possible path to the priority queue
                vector<string> next_path = current_path;
                next_path.push_back(next_station);
                pq.push(make_tuple(next_departure_time, next_departure_time - current_time, next_station, next_path));
            }

            // Add the departure time to the station
            station.departure_times.push(current_time + waiting_time + 1);
        }
    }

    return optimal_paths;
}


int main() {
// Create some sample data
vector<string> station_names = {"A", "B", "C", "D", "E", "F", "G"};
vector<tuple<string, string, int>> path_tuples = {make_tuple("A", "B", 5), make_tuple("A", "C", 4), make_tuple("B", "D", 3), make_tuple("C", "E", 6), make_tuple("D", "F", 4), make_tuple("E", "F", 2), make_tuple("F", "G", 5)};
vector<pair<string, string>> vehicles = {make_pair("A", "F"), make_pair("B", "E")};


// Add the stations and paths
vector<Station> stations;
Points(stations, station_names);

vector<Path> paths;
Paths(paths, path_tuples);

// Calculate the optimal paths for the vehicles
auto start_time = chrono::high_resolution_clock::now();
vector<tuple<pair<string, string>, vector<string>, int>> optimal_paths = Calculate(paths, stations, vehicles);
auto end_time = chrono::high_resolution_clock::now();
auto duration = chrono::duration_cast<chrono::microseconds>(end_time - start_time).count();

// Print the optimal paths
for (auto path : optimal_paths) {
    auto vehicle = get<0>(path);
    auto stations = get<1>(path);
    auto travel_time = get<2>(path);

    cout << "Optimal path for vehicle " << vehicle.first << " to " << vehicle.second << " is: ";
    for (auto station : stations) {
        cout << station << " ";
    }
    cout << "with a travel time of " << travel_time << endl;
}

cout << "Program took " << duration << " microseconds to complete" << endl;

return 0;









