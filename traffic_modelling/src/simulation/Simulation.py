from models import Junction
from models import Vehicle

class Simulation:
    def __init__(self, junction : Junction, simulation_duration : int = 3600):
        self.time = 0           # Time in seconds
        self.cycle_length = 10  # Length of a cycle in seconds
        self.junction = junction 
        self.simulation_duration = simulation_duration

        # Queues for each approach and movement
        self.queues = {
            'north': [],
            'south': [],
            'east': [],
            'west': []
        }

        # Record wait times per direction.
        self.wait_times = {
            'north': [],
            'south': [],
            'east': [],
            'west': []
        }

        # Track maximum queue lengths encountered during simulation.
        self.max_queue_lengths = {
            'north': 0,
            'south': 0,
            'east': 0,
            'west': 0
        }

        # For each direction, compute total vehicles per hour
        self.traffic_data = {
            'north': junction.north_traffic,
            'south': junction.south_traffic,
            'east':  junction.east_traffic,
            'west':  junction.west_traffic
        }
    
    def runSimulation(self):
        # For each direction and turn, compute the deterministic arrival times
        # Formula for scheduling vehicles: arrival_time = (3600 / vehicles per hour)
        next_arrivals = {}     # next_arrivals[direction][movement] = next arrival time
        arrival_intervals = {} # arrival_intervals[direction][movement] = time between arrivals
        movements = ["straight", "right", "left"]

        # Initialize next_arrivals and arrival_intervals
        for direction, flows in self.traffic_data.items():
            next_arrivals[direction] = {}
            arrival_intervals[direction] = {}
            for i, m in enumerate(movements):
                flow = flows[i]
                if flow > 0:
                    interval = 3600 / flow # seconds between arrivals
                    next_arrivals[direction][m] = 0.0
                else:
                    interval = None
                    next_arrivals[direction][m] = None
                arrival_intervals[direction][m] = interval
        
        # Fixed turning cost
        right_turn_cost = 2
        left_turn_cost = 1

        for t in range(self.simulation_duration):
            self.time = t

            # Add new vehicle for arrival
            for direction in ["north", "south", "east", "west"]:
                for m in movements:
                    interval = arrival_intervals[direction][m]
                    if interval is None:
                        continue

                    while next_arrivals[direction][m] is not None and next_arrivals[direction][m] <= t:
                        # Add vehicle to queue
                        arrival_time = next_arrivals[direction][m]
                        vehicle = Vehicle(entry=arrival_time, movement=m)
                        self.queues[direction].append(vehicle)
                        # Schedule next arrival
                        next_arrivals[direction][m] += interval
                
                # Sort queue by arrival time
                self.queues[direction].sort(key=lambda v: v.entry)
                # Update the maximum queue length
                if len(self.queues[direction]) > self.max_queue_lengths[direction]:
                    self.max_queue_lengths[direction] = len(self.queues[direction])
            
            # Update the active phase of the traffic light
            phase_time = t % self.cycle_length
            if phase_time < (self.cycle_length / 2):
                active_phase = ["north", "south"]
            else:
                active_phase = ["east", "west"]
            
            # Process vehicles in the queue
            for direction in active_phase:
                if self.queues[direction]:
                    vehicle = self.queues[direction].pop(0)

                    # Determine cost depending on turn direction
                    if vehicle.movement == "right":
                        cost = right_turn_cost
                    elif vehicle.movement == "left":
                        cost = left_turn_cost
                    else:
                        cost = 0
                    exit_time = t + cost
                    vehicle.setExit(exit_time)
                    wait_time = vehicle.getWaitTime()
                    self.wait_times[direction].append(wait_time)

    def calculateAverageWaitTime(self):
        """ Returns the average wait time per direction as (float, float, float, float) """
        pass

    def calculateMaxWaitTimes(self):
        """ Returns the maximum wait times per direction as (int, int, int, int) """
        pass

    def calculateMaxQueueLengths(self):
        """ Returns the maximum queue lengths per direction as (int, int, int, int) """
        pass

    def getActivePhase(self):
        """ Returns the active phase of the traffic light """
        return self.time % self.cycle_length

    def getInput(self, input):
        pass