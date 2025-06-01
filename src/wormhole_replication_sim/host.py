#host.py

from typing import Set

class Host:
    def __init__(
        self,
        host_id: str,
        uptime: int,
        downtime: int,
        uptime_cycle_counter: int,
        ):

        self.host_id = host_id
        self.uptime = uptime
        self.downtime = downtime
        self.is_online = True
        self.uptime_cycle_counter = uptime_cycle_counter
        self.hosted_file = set()
        self.hosted_chunks = set()

    def cycle_uptime(self):
        self.uptime_cycle_counter += 1

        if self.is_online:
            if self.uptime_cycle_counter >= self.uptime:
                self.is_online = False
                self.uptime_cycle_counter = 0
        else:
            if self.uptime_cycle_counter >= self.downtime:
                self.is_online = True
                self.uptime_cycle_counter = 0

    def __repr__(self):
        return (
            f"Host("
            f"id={self.host_id}, "
            f"online={self.is_online}, "
            f"uptime={self.uptime}, "
            f"downtime={self.downtime}, "
            f"uptime_counter={self.uptime_cycle_counter}, "
            f"hosted_files={len(self.hosted_file)}"
            f")"
        )

