#!/bin/python3

from traffic_sim.road import Road
from traffic_sim.junction import Junction
from traffic_sim.source import SmartSource
from traffic_sim.sink import Sink
from traffic_sim.engine import Simulation
from traffic_sim.routing import Router
from traffic_sim.visualization import Visualizer
from traffic_sim.layout import compute_layout

vehicle_counter = [0]

# -------------------------------
# ROADS
# -------------------------------
r1 = Road(1, 8, 3, 6)
r2 = Road(2, 7, 6, 6)
r3 = Road(3, 6, 3, 6)
r4 = Road(4, 3, 4, 6)
r5 = Road(5, 4, 5, 6)
r6 = Road(6, 3, 2, 6)

roads = [r1, r2, r3, r4, r5, r6]

# -------------------------------
# ROUTER
# -------------------------------
router = Router(roads)

# -------------------------------
# JUNCTIONS
# -------------------------------
junctions = [
    Junction(3, [r1, r3], {4: r4, 6: r6}),
    Junction(4, [r4], {5: r5}),
    Junction(6, [r2], {3: r3})
]

# -------------------------------
# SOURCES
# -------------------------------
src_left = SmartSource(
    id=8,
    mean=0.5,
    to_road=r1,
    router=router,
    vehicle_counter=vehicle_counter,
    destination=5
)

src_bottom = SmartSource(
    id=7,
    mean=0.5,
    to_road=r2,
    router=router,
    vehicle_counter=vehicle_counter,
    destination=2
)

sources = [src_left, src_bottom]

# -------------------------------
# SINKS
# -------------------------------
sink_top = Sink(2, r6)
sink_right = Sink(5, r5)

sinks = [sink_top, sink_right]

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

positions = compute_layout(junction_ids, roads)

# -------------------------------
# VISUALIZATION
# -------------------------------
viz = Visualizer(roads, positions, sources, sinks)
viz.animate(sim, steps=140, save_path="traffic.gif")

# -------------------------------
# STATS
# -------------------------------
print("\n--- Simulation Stats ---")
for s in sinks:
    s.print_stats()