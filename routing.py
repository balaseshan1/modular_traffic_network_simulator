import heapq

class Router:
    def __init__(self, roads):
        self.graph = {}

        for r in roads:
            if r.from_junction not in self.graph:
                self.graph[r.from_junction] = []

            self.graph[r.from_junction].append(
                (r.to_junction, r.id, r.capacity)
            )

    def shortest_path(self, start, end):
        pq = [(0, start, [])]
        visited = set()

        while pq:
            cost, node, path = heapq.heappop(pq)

            if node in visited:
                continue
            visited.add(node)

            if node == end:
                return path

            for nxt, road_id, w in self.graph.get(node, []):
                if nxt not in visited:
                    heapq.heappush(pq, (cost + w, nxt, path + [road_id]))

        return []