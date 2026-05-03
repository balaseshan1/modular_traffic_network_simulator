"""import numpy as np
from traffic_sim.vehicle import Vehicle


class SmartSource:
    def __init__(self, id, mean, to_road, router, vehicle_counter, destination):
        self.id = id
        self.mean = mean  # λ (lambda)
        self.to_road = to_road
        self.router = router
        self.vehicle_counter = vehicle_counter
        self.destination = destination

    def generate(self, tick):
        # Poisson random variable
        X = np.random.poisson(self.mean)

        # generate up to X vehicles (respect road capacity)
        for _ in range(X):
            if not self.to_road.can_enter():
                return

            route = self.router.shortest_path(
                self.to_road.from_junction,
                self.destination
            )

            if not route:
                return

            #print(f"[ROUTE] Vehicle {self.vehicle_counter[0]}: {self.id} -> {self.destination} via {route}")

            v = Vehicle(
                id=self.vehicle_counter[0],
                source=self.id,
                destination=self.destination,
                route=route,
                spawn_time=tick
            )

            self.vehicle_counter[0] += 1
            self.to_road.enter(v)
"""

import numpy as np
import random
from traffic_sim.vehicle import Vehicle


# ---------------------------------
# LOGICAL SOURCE (flow generator)
# ---------------------------------
class SmartSource:
    def __init__(self, id, mean, router, vehicle_counter, destination):
        self.id = id
        self.mean = mean
        self.router = router
        self.vehicle_counter = vehicle_counter
        self.destination = destination

        # stats
        self.generated = 0
        self.sent = 0


# ---------------------------------
# PHYSICAL SOURCE NODE (contention)
# ---------------------------------
class SourceNode:
    def __init__(self, node_id, sources, to_road):
        self.node_id = node_id
        self.sources = sources  # list of SmartSource
        self.to_road = to_road

    def generate(self, tick):
        contenders = []

        # Step 1: each logical source tries to transmit
        for s in self.sources:
            X = np.random.poisson(s.mean)

            if X > 0:
                contenders.append(s)
                s.generated += 1

        if not contenders:
            return

        # Step 2: collision resolution
        chosen = random.choice(contenders)

        # Step 3: check road capacity
        if not self.to_road.can_enter():
            return

        # Step 4: routing
        route = chosen.router.shortest_path(
            self.to_road.from_junction,
            chosen.destination
        )

        if not route:
            return

        # Step 5: create vehicle
        v = Vehicle(
            id=chosen.vehicle_counter[0],
            source=chosen.id,
            destination=chosen.destination,
            route=route,
            spawn_time=tick
        )

        chosen.vehicle_counter[0] += 1
        chosen.sent += 1

        self.to_road.enter(v)

    def print_stats(self):
        print(f"\nSource Node {self.node_id}")
        for s in self.sources:
            print(f"  {s.id}:")
            print(f"    Generated: {s.generated}")
            print(f"    Sent: {s.sent}")