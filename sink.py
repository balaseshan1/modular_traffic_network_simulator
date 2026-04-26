class Sink:
    def __init__(self, id, from_road):
        self.id = id
        self.from_road = from_road
        self.total = 0
        self.total_time = 0

    def collect(self, tick):
        v = self.from_road.peek()
        if v:
            self.from_road.pop()
            self.total += 1
            self.total_time += (tick - v.spawn_time)

    def print_stats(self):
        if self.total == 0:
            print(f"Sink {self.id}: No vehicles")
        else:
            print(f"Sink {self.id}:")
            print(f"  Vehicles: {self.total}")
            print(f"  Avg wait time: {self.total_time / self.total:.2f}")