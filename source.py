import numpy as np
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

            v = Vehicle(
                id=self.vehicle_counter[0],
                source=self.id,
                destination=self.destination,
                route=route,
                spawn_time=tick
            )

            self.vehicle_counter[0] += 1
            self.to_road.enter(v)