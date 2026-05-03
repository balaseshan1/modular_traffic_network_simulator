import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import random
from matplotlib.lines import Line2D


class Visualizer:
    def __init__(self, roads, junction_positions, sources=None, sinks=None):
        self.roads = roads
        self.junction_positions = junction_positions

        # group roads for bidirectional detection
        self.road_groups = {}
        for r in roads:
            key = tuple(sorted([r.from_junction, r.to_junction]))
            self.road_groups.setdefault(key, []).append(r)

        # source → sink mapping
        self.source_sink_pairs = []
        if sources:
            for node in sources:
                for s in node.sources:
                    self.source_sink_pairs.append((s.id, s.destination))

        # assign stable colors per logical source
        self.source_colors = {}
        for src, _ in self.source_sink_pairs:
            self.source_colors[src] = (
                random.uniform(0.2, 0.9),
                random.uniform(0.2, 0.9),
                random.uniform(0.2, 0.9),
            )

    # ---------------------------------
    # COLOR PER SOURCE
    # ---------------------------------
    def get_color(self, vehicle):
        base = self.source_colors.get(vehicle.source, (0.5, 0.5, 0.5))

        variation = (vehicle.id % 10) * 0.02

        return (
            min(1.0, base[0] + variation),
            min(1.0, base[1] + variation),
            min(1.0, base[2] + variation),
        )

    # ---------------------------------
    # PERPENDICULAR OFFSET
    # ---------------------------------
    def get_offset(self, x1, y1, x2, y2, direction):
        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)

        if length == 0:
            return 0, 0

        # perpendicular unit vector
        px = -dy / length
        py = dx / length

        offset_mag = 0.15

        return px * offset_mag * direction, py * offset_mag * direction

    # ---------------------------------
    # DRAW FRAME
    # ---------------------------------
    def draw_frame(self, ax):
        ax.clear()

        # -------------------------
        # DRAW ROADS + VEHICLES
        # -------------------------
        for key, roads in self.road_groups.items():
            r0 = roads[0]

            x1, y1 = self.junction_positions[r0.from_junction]
            x2, y2 = self.junction_positions[r0.to_junction]

            if len(roads) == 1:
                offsets = [(0, 0)]
            else:
                offsets = []
                for r in roads:
                    if r.from_junction == r0.from_junction:
                        offsets.append(self.get_offset(x1, y1, x2, y2, +1))
                    else:
                        offsets.append(self.get_offset(x1, y1, x2, y2, -1))

            for r, (ox, oy) in zip(roads, offsets):
                x1r = x1 + ox
                y1r = y1 + oy
                x2r = x2 + ox
                y2r = y2 + oy

                ax.plot([x1r, x2r], [y1r, y2r], 'k-', linewidth=2)

                dx = x2r - x1r
                dy = y2r - y1r

                for i, v in enumerate(r.slots):
                    if v is not None:
                        t = (i + 0.5) / r.capacity
                        x = x1r + t * dx
                        y = y1r + t * dy

                        ax.scatter(x, y, color=self.get_color(v), s=40)

        # -------------------------
        # DRAW JUNCTIONS
        # -------------------------
        for j, (x, y) in self.junction_positions.items():
            ax.scatter(x, y, color='black', s=60)
            ax.text(x + 0.1, y + 0.1, str(j), fontsize=8)

        ax.set_title("Traffic Simulation")
        ax.set_aspect('equal')
        xs = [x for (x, y) in self.junction_positions.values()]
        ys = [y for (x, y) in self.junction_positions.values()]

        margin = 1

        ax.set_xlim(min(xs) - margin, max(xs) + margin)
        ax.set_ylim(min(ys) - margin, max(ys) + margin)

        # -------------------------
        # LEGEND (FIXED)
        # -------------------------
        legend_elements = []

        for src, dst in self.source_sink_pairs:
            color = self.source_colors[src]

            legend_elements.append(
                Line2D(
                    [0], [0],
                    marker='o',
                    color='w',
                    label=f"{src} → {dst}",
                    markerfacecolor=color,
                    markersize=8
                )
            )

        ax.legend(
            handles=legend_elements,
            loc='upper left',
            bbox_to_anchor=(1.02, 1),
            borderaxespad=0.,
            framealpha=0.8
        )

    # ---------------------------------
    # ANIMATION
    # ---------------------------------
    def animate(self, sim, steps=100, save_path="traffic.gif"):
        fig, ax = plt.subplots()  # original size

        plt.subplots_adjust(right=0.75)

        # legend
        legend_elements = []
        for src, dst in self.source_sink_pairs:
            color = self.source_colors[src]

            legend_elements.append(
                Line2D(
                    [0], [0],
                    marker='o',
                    color='w',
                    label=f"{src} → {dst}",
                    markerfacecolor=color,
                    markersize=8
                )
            )

        ax.legend(
            handles=legend_elements,
            loc='upper left',
            bbox_to_anchor=(1.02, 1),
            borderaxespad=0.,
            framealpha=0.8
        )

        def update(frame):
            sim.step()
            self.draw_frame(ax)

        ani = animation.FuncAnimation(
            fig,
            update,
            frames=steps,
            repeat=False
        )

        ani.save(save_path, writer='pillow', fps=5)

        print(f"Saved animation to {save_path}")
