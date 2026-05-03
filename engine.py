class Simulation:
    def __init__(self, roads, junctions, sources, sinks):
        self.roads = roads
        self.junctions = junctions
        self.sources = sources
        self.sinks = sinks
        self.tick = 0

    def step(self):
        self.tick += 1

        # 1. Junction scheduling (decide movements → buffer)
        for j in self.junctions:
            j.schedule()

        # 2. Move vehicles along roads
        for r in self.roads:
            r.tick()

        # 3. Apply buffered entries (vehicles enter at next tick)
        for r in self.roads:
            if hasattr(r, "apply_incoming"):
                r.apply_incoming()

        # 4. Generate new vehicles
        for s in self.sources:
            s.generate(self.tick)

        # 5. Collect at sinks
        for s in self.sinks:
            s.collect(self.tick)
        """
        print(self.roads[7].id, [x.id if x else None for x in self.roads[7].slots])
        print(self.roads[6].id, [x.id if x else None for x in self.roads[6].slots])
        print(self.roads[16].id, [x.id if x else None for x in self.roads[16].slots])
        print(self.roads[8].id, [x.id if x else None for x in self.roads[8].slots])
        print()"""
