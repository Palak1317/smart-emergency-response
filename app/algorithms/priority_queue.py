import heapq


class EmergencyPriorityQueue:

    PRIORITY = {
        "CRITICAL": 1,
        "HIGH": 2,
        "MEDIUM": 3,
        "LOW": 4
    }

    def __init__(self):
        self.heap = []

    def add_emergency(self, emergency):
        priority = self.PRIORITY.get(
            emergency.severity.upper(),
            4
        )

        heapq.heappush(
            self.heap,
            (priority, emergency.created_at, emergency.id, emergency)
        )

    def get_next_emergency(self):
        if not self.heap:
            return None

        return heapq.heappop(self.heap)[3]

    def is_empty(self):
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)