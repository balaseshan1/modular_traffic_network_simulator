import random
import math


def compute_layout(junction_ids, roads, iterations=200, width=10, height=10):
    """
    Force-directed layout with:
    - Repulsion between all nodes
    - Attraction along roads (capacity-based length)
    - Boundary clamping
    - Cooling for stability
    """

    # -----------------------------
    # INITIALIZE RANDOM POSITIONS
    # -----------------------------
    pos = {
        j: [
            random.uniform(1, width - 1),
            random.uniform(1, height - 1)
        ]
        for j in junction_ids
    }

    n = len(junction_ids)
    area = width * height
    k = math.sqrt(area / n)  # ideal spacing

    # -----------------------------
    # MAIN ITERATIONS
    # -----------------------------
    for it in range(iterations):
        disp = {j: [0.0, 0.0] for j in junction_ids}

        # -------------------------
        # REPULSION (node-node)
        # -------------------------
        for i in junction_ids:
            for j in junction_ids:
                if i == j:
                    continue

                dx = pos[i][0] - pos[j][0]
                dy = pos[i][1] - pos[j][1]

                dist = math.sqrt(dx * dx + dy * dy) + 1e-6

                force = (k * k) / dist

                disp[i][0] += (dx / dist) * force
                disp[i][1] += (dy / dist) * force

        # -------------------------
        # ATTRACTION (edges)
        # -------------------------
        for r in roads:
            u = r.from_junction
            v = r.to_junction

            dx = pos[u][0] - pos[v][0]
            dy = pos[u][1] - pos[v][1]

            dist = math.sqrt(dx * dx + dy * dy) + 1e-6

            # capacity affects desired length
            desired_length = r.capacity * 0.6

            force = (dist - desired_length)

            disp[u][0] -= (dx / dist) * force
            disp[u][1] -= (dy / dist) * force

            disp[v][0] += (dx / dist) * force
            disp[v][1] += (dy / dist) * force

        # -------------------------
        # COOLING (reduces movement)
        # -------------------------
        cooling = 0.05 * (1 - it / iterations)

        # -------------------------
        # UPDATE POSITIONS + CLAMP
        # -------------------------
        for j in junction_ids:
            pos[j][0] += disp[j][0] * cooling
            pos[j][1] += disp[j][1] * cooling

            # clamp within bounds (margin = 0.5)
            pos[j][0] = max(0.5, min(width - 0.5, pos[j][0]))
            pos[j][1] = max(0.5, min(height - 0.5, pos[j][1]))

    # -----------------------------
    # OPTIONAL: CENTERING
    # -----------------------------
    avg_x = sum(p[0] for p in pos.values()) / n
    avg_y = sum(p[1] for p in pos.values()) / n

    shift_x = (width / 2) - avg_x
    shift_y = (height / 2) - avg_y

    for j in pos:
        pos[j][0] += shift_x
        pos[j][1] += shift_y

        # clamp again after centering
        pos[j][0] = max(0.5, min(width - 0.5, pos[j][0]))
        pos[j][1] = max(0.5, min(height - 0.5, pos[j][1]))

    return pos