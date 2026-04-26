class Road:
    def __init__(self, id, from_junction, to_junction, capacity):
        self.id = id
        self.from_junction = from_junction
        self.to_junction = to_junction
        self.capacity = capacity

        # slots represent positions on road
        self.slots = [None] * capacity

        # buffer for delayed entry (t → t+1)
        self.incoming_buffer = []

    def can_enter(self):
        """
        Check if first slot is empty
        """
        return self.slots[0] is None

    def enter(self, vehicle):
        """
        Add vehicle to buffer (NOT directly to road)
        """
        self.incoming_buffer.append(vehicle)

    def apply_incoming(self):
        """
        Move one vehicle from buffer to slot 0 (if possible)
        """
        if self.incoming_buffer and self.can_enter():
            v = self.incoming_buffer.pop(0)
            v.pos = 0
            self.slots[0] = v

    def tick(self):
        """
        Move vehicles forward by one slot (from end to start)
        """
        for i in range(self.capacity - 1, 0, -1):
            if self.slots[i] is None and self.slots[i - 1] is not None:
                self.slots[i] = self.slots[i - 1]
                self.slots[i - 1] = None

    def peek(self):
        """
        Look at vehicle at last slot (near junction)
        """
        return self.slots[-1]

    def pop(self):
        """
        Remove vehicle from last slot
        """
        v = self.slots[-1]
        self.slots[-1] = None
        return v