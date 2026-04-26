import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Visualizer:
    def __init__(self, roads, junction_positions, sources=None, sinks=None):
        self.roads = roads
        self.junction_positions = junction_positions

        # store mappings
        self.source_sink_pairs = []
        if sources:
            for s in sources:
                self.source_sink_pairs.append((s.id, s.destination))

    # ---------------------------------
    # COLOR (destination + variation)
    # ---------------------------------
    def get_color(self, vehicle):
        base_colors = {
            2: (1.0, 0.2, 0.2),  # red-ish
            5: (0.2, 0.2, 1.0),  # blue-ish
        }

        base = base_colors.get(vehicle.destination, (0.2, 0.8, 0.2))
        variation = (vehicle.id % 10) * 0.02

        return (
            min(1.0, base[0] + variation),
            min(1.0, base[1] + variation),
            min(1.0, base[2] + variation),
        )

    # ---------------------------------
    # DRAW FRAME
    # ---------------------------------
    def draw_frame(self, ax):
        ax.clear()

        # DRAW ROADS
        for r in self.roads:
            x1, y1 = self.junction_positions[r.from_junction]
            x2, y2 = self.junction_positions[r.to_junction]

            ax.plot([x1, x2], [y1, y2], 'k-', linewidth=2)

            dx = x2 - x1
            dy = y2 - y1

            # DRAW VEHICLES
            for i, v in enumerate(r.slots):
                if v is not None:
                    t = (i + 0.5) / r.capacity
                    x = x1 + t * dx
                    y = y1 + t * dy

                    ax.scatter(x, y, color=self.get_color(v), s=40)

        # DRAW JUNCTIONS
        for j, (x, y) in self.junction_positions.items():
            ax.scatter(x, y, color='black', s=60)
            ax.text(x + 0.1, y + 0.1, str(j), fontsize=8)

        ax.set_title("Traffic Simulation (Auto Layout)")
        ax.set_aspect('equal')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)

        """
        # -------------------------
        # LEGEND: Source -> Sink
        # -------------------------
        if self.source_sink_pairs:
            legend_text = "Source → Sink\n"
            for src, dst in self.source_sink_pairs:
                legend_text += f"{src} → {dst}\n"

            ax.text(
                0.02, 0.98,
                legend_text.strip(),
                transform=ax.transAxes,
                fontsize=8,
                verticalalignment='top',
                bbox=dict(facecolor='white', alpha=0.7)
            )
        """

    # ---------------------------------
    # ANIMATION
    # ---------------------------------
    def animate(self, sim, steps=100, save_path="traffic.gif"):
        fig, ax = plt.subplots()

        # leave space on right for legend
        plt.subplots_adjust(right=0.75)

        # -------------------------
        # CREATE LEGEND TEXT
        # -------------------------
        legend_text = "Source → Sink\n"
        for src, dst in self.source_sink_pairs:
            legend_text += f"{src} → {dst}\n"

        # place outside plot
        fig.text(
            0.78, 0.8,
            legend_text.strip(),
            fontsize=10,
            verticalalignment='top',
            bbox=dict(facecolor='white', alpha=0.8)
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
