from dataclasses import dataclass

@dataclass
class Vehicle:
    id: int
    source: int
    destination: int
    route: list
    route_index: int = 0
    spawn_time: int = 0
    pos: int = 0
    wait_time: int = 0