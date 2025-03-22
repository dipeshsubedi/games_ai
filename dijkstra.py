class Graph:
    def __init__(self, size):
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [''] * size

    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            self.adj_matrix[v][u] = weight  # For undirected graph

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def dijkstra(self, start_vertex_data):
        # Find the index of the starting vertex based on its name
        start_vertex = self.vertex_data.index(start_vertex_data)

        # Create a list to store the shortest known distance to each vertex
        # Initially, set all distances to infinity (unknown)
        distances = [float('inf')] * self.size

        # The distance to the start vertex itself is 0
        distances[start_vertex] = 0

        # Keep track of which vertices have been visited
        visited = [False] * self.size

        # Loop to process each vertex
        for _ in range(self.size):
            # Start by assuming no unvisited vertex has a small distance
            min_distance = float('inf')
            u = None  # This will hold the closest unvisited vertex

            # Find the unvisited vertex with the smallest known distance
            for i in range(self.size):
                if not visited[i] and distances[i] < min_distance:
                    min_distance = distances[i]
                    u = i  # Store the index of this closest vertex

            # If we didn't find any reachable unvisited vertex, exit the loop
            if u is None:
                break

            # Mark this vertex as visited, meaning its shortest distance is finalized
            visited[u] = True

            # Check all neighbors of this vertex
            for v in range(self.size):
                # If there's a connection (non-zero weight) and the neighbor isn't visited
                if self.adj_matrix[u][v] != 0 and not visited[v]:
                    # Calculate the new possible shortest distance via vertex `u`
                    alt = distances[u] + self.adj_matrix[u][v]

                    # If this new distance is shorter, update it
                    if alt < distances[v]:
                        distances[v] = alt

        # Return the final list of shortest distances from the start vertex
        return distances


g = Graph(7)

g.add_vertex_data(0, 'A')
g.add_vertex_data(1, 'B')
g.add_vertex_data(2, 'C')
g.add_vertex_data(3, 'D')
g.add_vertex_data(4, 'E')
g.add_vertex_data(5, 'F')
g.add_vertex_data(6, 'G')

g.add_edge(3, 0, 4)  # D - A, weight 4
g.add_edge(3, 4, 2)  # D - E, weight 2
g.add_edge(0, 2, 3)  # A - C, weight 3
g.add_edge(0, 4, 4)  # A - E, weight 4
g.add_edge(2, 4, 4)  # C - E, weight 4
g.add_edge(4, 6, 5)  # E - G, weight 5
g.add_edge(2, 5, 5)  # C - F, weight 5
g.add_edge(2, 1, 2)  # C - B, weight 2
g.add_edge(1, 5, 2)  # B - F, weight 2
g.add_edge(6, 5, 5)  # G - F, weight 5

# Start Dijkstra's algorithm from vertex 'D' and show the results
print("Dijkstra's Algorithm starting from vertex D:\n")  # Print a message before showing distances

distances = g.dijkstra('D')  # Run Dijkstra’s algorithm starting from 'D' to find shortest paths

# Go through each vertex and display the shortest distance from 'D'
for i, d in enumerate(distances):  
    print(f"Shortest distance from D to {g.vertex_data[i]}: {d}")  # Show the result in a readable format
