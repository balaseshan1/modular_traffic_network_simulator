# Traffic Simulator

A modular traffic simulation system for a directed road network with multiple junctions, sources, and sinks. The simulator models vehicle movement using a time-step engine and visualizes traffic flow as an animated GIF.

## Features

- Directed roads with capacity constraints
- Junctions with round-robin scheduling
- Vehicles with source to destination routing
- Poisson-based traffic generation
- Sink nodes with statistics collection
- Time-step simulation engine
- Automatic network layout (no manual coordinates)
- Animated visualization (GIF output)

## Project Structure
```
traffic_sim/
    road.py
    junction.py
    vehicle.py
    source.py
    sink.py
    routing.py
    engine.py
    visualization.py
    layout.py

main.py
README.md
```
## Requirements

Python 3.x

Install dependencies:

pip install matplotlib numpy

## How to Run

python main.py

## Output

- traffic.gif: animated simulation
- Console output:
  - Average waiting time per sink
  - Total number of cars arrived per sink

## Simulation Model

### Vehicles
Each vehicle has:
- Source
- Destination
- Route
Vehicles move one slot per tick.

### Roads
- Fixed-size slot arrays
- Vehicles move forward if space is available
- Each road has capacity and direction

### Junctions
- One vehicle moves per tick
- Round-robin scheduling across incoming roads
- One-tick delayed transfer using buffers

### Sources
- Generate vehicles using Poisson distribution
- Mean rate controls traffic intensity

### Sinks
- Collect exiting vehicles
- Compute statistics such as travel time

### Simulation Engine

Each tick:
1. Junction scheduling
2. Road movement
3. Apply buffered transfers
4. Generate vehicles
5. Collect at sinks

## Visualization

- Roads are lines between junctions
- Vehicles are colored points
- Color indicates destination with slight variation
- Layout computed automatically
