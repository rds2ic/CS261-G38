class StatsCollector:
    def __init__(self, simulation):
        """
        Initialize with a Simulation instance.
        """
        self.simulation = simulation

    def calculateAverageWaitTime(self):
        """Returns a dictionary mapping each direction to the average wait time (in seconds)."""
        avg_wait_times = {}
        for direction in ["north", "south", "east", "west"]:
            wait_times = self.simulation.wait_times[direction]
            avg_wait_time = sum(wait_times) / len(wait_times) if wait_times else None
            avg_wait_times[direction] = avg_wait_time
        return avg_wait_times

    def calculateMaxWaitTimes(self):
        """Returns a dictionary mapping each direction to the maximum wait time (in seconds)."""
        max_wait_times = {}
        for direction in ["north", "south", "east", "west"]:
            wait_times = self.simulation.wait_times[direction]
            max_wait_time = max(wait_times) if wait_times else None
            max_wait_times[direction] = max_wait_time
        return max_wait_times

    def getMaxQueueLengths(self):
        """Returns a dictionary mapping each direction to the maximum queue length recorded."""
        return self.simulation.max_queue_lengths

    def getActivePhase(self):
        """
        Returns the active phase of the traffic light.
        'NS' if north-south are green, and 'EW' if east-west are green.
        """
        phase_time = self.simulation.time % self.simulation.cycle_length
        return "NS" if phase_time < (self.simulation.cycle_length / 2) else "EW"
