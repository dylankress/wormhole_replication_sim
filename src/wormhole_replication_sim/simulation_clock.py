#simulation_clock.py

class SimulationClock:
    def __init__(self):
        self.current_tick = 0  # Start at tick 0

    def tick(self):
        self.current_tick += 1

    def get_time(self):
        # Return time in seconds (1 tick = 1 second)
        return self.current_tick

    def reset(self):
        self.current_tick = 0

    def __repr__(self):
        return f"SimulationClock(current_tick={self.current_tick})"

