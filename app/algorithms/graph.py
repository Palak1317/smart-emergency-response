import heapq


class Graph:

    def __init__(self):
        self.graph = {}

    def add_edge(self, source, destination, distance):
        if source not in self.graph:
            self.graph[source] = []

        if destination not in self.graph:
            self.graph[destination] = []

        self.graph[source].append(
            (destination, distance)
        )

        self.graph[destination].append(
            (source, distance)
        )

    def dijkstra(self, start, end):

        distances = {
            node: float("inf")
            for node in self.graph
        }

        previous = {
            node: None
            for node in self.graph
        }

        distances[start] = 0

        priority_queue = [
            (0, start)
        ]

        while priority_queue:

            current_distance, current_node = heapq.heappop(
                priority_queue
            )

            if current_distance > distances[current_node]:
                continue

            if current_node == end:
                break

            for neighbor, edge_distance in self.graph[current_node]:

                new_distance = (
                    current_distance + edge_distance
                )

                if new_distance < distances[neighbor]:

                    distances[neighbor] = new_distance

                    previous[neighbor] = current_node

                    heapq.heappush(
                        priority_queue,
                        (new_distance, neighbor)
                    )

        if distances[end] == float("inf"):
            return None

        path = []

        current = end

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

        return {
            "distance": distances[end],
            "path": path
        }