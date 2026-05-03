#!/bin/python3

from traffic_sim.road import Road
from traffic_sim.junction import Junction
from traffic_sim.source import SmartSource, SourceNode
from traffic_sim.sink import Sink
from traffic_sim.engine import Simulation
from traffic_sim.routing import Router
from traffic_sim.visualization import Visualizer
from traffic_sim.layout import compute_layout

ROAD_CAPACITY = 5
RATE_GENERATION = 0.2 # rate at which vehicles are generated at each source (poisson process)

vehicle_counter = [0]
# -------------------------------
# ROADS
# -------------------------------
r1 = Road(1, "SN14", "J0", ROAD_CAPACITY)

r2 = Road(2, "J0", "J1", ROAD_CAPACITY)
r3 = Road(3, "J1", "J0", ROAD_CAPACITY)

r4 = Road(4, "J1", "K2", ROAD_CAPACITY)

r5 = Road(5, "SN25", "J2", ROAD_CAPACITY)

r6 = Road(6, "J2", "J3", ROAD_CAPACITY)
r7 = Road(7, "J3", "J2", ROAD_CAPACITY)

r8 = Road(8, "SN3", "J3", ROAD_CAPACITY)

r9 = Road(9, "J4", "K34", ROAD_CAPACITY)

r10 = Road(10, "J4", "J5", ROAD_CAPACITY)
r11 = Road(11, "J5", "J4", ROAD_CAPACITY)

r12 = Road(12, "J5", "K15", ROAD_CAPACITY)

r13 = Road(13, "J0", "J2", ROAD_CAPACITY)
r14 = Road(14, "J2", "J0", ROAD_CAPACITY)

r15 = Road(15, "J1", "J3", ROAD_CAPACITY)
r16 = Road(16, "J3", "J1", ROAD_CAPACITY)

r17 = Road(17, "J2", "J4", ROAD_CAPACITY)
r18 = Road(18, "J4", "J2", ROAD_CAPACITY)

r19 = Road(19, "J3", "J5", ROAD_CAPACITY)
r20 = Road(20, "J5", "J3", ROAD_CAPACITY)

roads = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20]

# -------------------------------
# ROUTER
# -------------------------------
router = Router(roads)

# -------------------------------
# JUNCTIONS
# -------------------------------
junctions = [
    Junction("J0", [r1, r3, r14], {2: r2, 13: r13}),
    Junction("J1", [r2, r16], {3: r3, 4: r4, 15: r15}),
    Junction("J2", [r5, r7, r13, r18], {6: r6, 14: r14, 17: r17}),
    Junction("J3", [r6, r8, r15, r20], {7: r7, 16: r16, 19: r19}),
    Junction("J4", [r17, r11], {9: r9, 10: r10, 18: r18}),
    Junction("J5", [r10, r19], {11: r11, 12: r12, 20: r20}),
]

# -------------------------------
# SOURCES
# -------------------------------
src_1 = SmartSource(
    id = "S1",
    mean = RATE_GENERATION,
    router = router,
    vehicle_counter = vehicle_counter,
    destination = "K15"
)

src_2 = SmartSource(
    id = "S2",
    mean = RATE_GENERATION,
    router = router,
    vehicle_counter = vehicle_counter,
    destination = "K2"
)

src_3 = SmartSource(
    id = "S3",
    mean = RATE_GENERATION,
    router = router,
    vehicle_counter = vehicle_counter,
    destination = "K34"
)

src_4 = SmartSource(
    id = "S4",
    mean = RATE_GENERATION,
    router = router,
    vehicle_counter = vehicle_counter,
    destination = "K34"
)

src_5 = SmartSource(
    id = "S5",
    mean = RATE_GENERATION,
    router = router,
    vehicle_counter = vehicle_counter,
    destination = "K15"
)

srcnode_25 = SourceNode(
    node_id = "SN25",
    sources = [src_2, src_5],
    to_road = r5
)

srcnode_14 = SourceNode(
    node_id = "SN14",
    sources = [src_1, src_4],
    to_road = r1
)

srcnode_3 = SourceNode(
    node_id = "SN3",
    sources = [src_3],
    to_road = r8
)

sources = [srcnode_14, srcnode_25, srcnode_3]

# -------------------------------
# SINKS
# -------------------------------
sink_15 = Sink("K15", r12)
sink_34 = Sink("K34", r9)
sink_2 = Sink("K2", r4)
sinks = [sink_15, sink_34, sink_2]


# -------------------------------
# SIMULATION
# -------------------------------
sim = Simulation(roads, junctions, sources, sinks)

# -------------------------------
# AUTO LAYOUT (NO MANUAL POSITIONS)
# -------------------------------
junction_ids = set()
for r in roads:
    junction_ids.add(r.from_junction)
    junction_ids.add(r.to_junction)

# positions = compute_layout(junction_ids, roads)
positions = {
    "SN14": (1, 9),
    "J0":  (3, 9),
    "J1":  (5, 9),
    "K2":  (7, 9),

    "SN25": (1, 7),
    "J2":  (3, 7),
    "J3":  (5, 7),
    "SN3":  (7, 7),

    "K34": (1, 5),
    "J4":  (3, 5),
    "J5":  (5, 5),
    "K15": (7, 5),
}
# -------------------------------
# VISUALIZATION
# -------------------------------
viz = Visualizer(roads, positions, sources, sinks)
viz.animate(sim, steps=100, save_path="traffic.gif")

# -------------------------------
# STATS
# -------------------------------
print("\n--- Simulation Stats ---")
for s in sources:
    s.print_stats()