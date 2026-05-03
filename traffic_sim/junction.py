class Junction:
    def __init__(self, id, incoming_roads, outgoing_roads):
        self.id = id
        self.incoming = incoming_roads
        self.outgoing = outgoing_roads
        self.last_served = -1  # round-robin pointer

    def schedule(self):
        n = len(self.incoming)

        # try roads in round-robin order
        for i in range(n):
            idx = (self.last_served + 1 + i) % n
            road = self.incoming[idx]

            v = road.peek()
            if v is None:
                continue

            # no next road → ignore
            if v.route_index + 1 >= len(v.route):
                continue

            next_road_id = v.route[v.route_index + 1]
            next_road = self.outgoing.get(next_road_id)

            if next_road and next_road.can_enter():
                # remove from current road
                road.pop()

                # update route
                v.route_index += 1

                # push to buffer (delayed entry)
                next_road.incoming_buffer.append(v)

                # update round-robin pointer
                self.last_served = idx

                # ONLY ONE vehicle per tick
                return
