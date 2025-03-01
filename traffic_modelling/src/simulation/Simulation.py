from models import Junction, Vehicle


class Simulation:
    def __init__(self, junction : Junction, simulation_duration : int = 3600):
        self.time = 0           # Time in seconds
        self.cycle_length = 10  # Length of a cycle in seconds
        self.junction = junction # Junction config to be used
        self.simulation_duration = simulation_duration # Duration of the simulation in seconds

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
        next_arrivals = {}     # next_arrivals[direction] = next arrival time
        arrival_intervals = {} # arrival_intervals[direction] = time between arrivals

        # Initialize next_arrivals and arrival_intervals
        for direction, flow in self.traffic_data.items():
            total_flow = sum(flow)
            if total_flow > 0:
                interval = 3600 / total_flow # seconds betweena arrivals for that direction
                next_arrivals[direction] = 0
                arrival_intervals[direction] = interval
            else:
                next_arrivals[direction] = None
                arrival_intervals[direction] = None
        
        # Fixed turning cost
        right_turn_cost = 2
        left_turn_cost = 1
        
        #fixed reaction time costs
        first_reaction_cost = 3  #first car reaction to traffic lights
        gap_reaction_cost = 2
        
        # Track when the last vehicle exited per direction
        last_exit_time = {
            'north': 0,
            'south': 0,
            'east': 0,
            'west': 0
        }

        # Main simulation loop
        for t in range(self.simulation_duration):
            self.time = t

            for direction in ["north", "south", "east", "west"]:
                interval = arrival_intervals[direction]
                if interval is None:
                    continue

                while next_arrivals[direction] is not None and next_arrivals[direction] <= t:
                    # Create a new vehicle
                    vehicle = Vehicle(t, direction)
                    self.queues[direction].append(vehicle)

                    # Schedule next arrival
                    next_arrivals[direction] += interval
                
                # Sort queue by arrival time
                self.queues[direction].sort(key=lambda v: v.entry)

                # Updae the maximum queue length
                self.max_queue_lengths[direction] = max(self.max_queue_lengths[direction], len(self.queues[direction]))
            
            phase_time = t % self.cycle_length
            if phase_time < (self.cycle_length / 2):
                active_phase = ["north", "south"]
            else:
                active_phase = ["east", "west"]
            
            # Process the active phase
            for direction in active_phase:
                if self.queues[direction]:
                    vehicle = self.queues[direction][0]  
                    
                    if last_exit_time[direction] == 0:
                        reaction_time = first_reaction_cost
                    else:
                        reaction_time = gap_reaction_cost

                    if t >= last_exit_time[direction] + reaction_time:
                        vehicle = self.queues[direction].pop(0)
                        
                        if vehicle.movement == "right":
                            cost = right_turn_cost
                        elif vehicle.movement == "left":
                            cost = left_turn_cost
                        else:
                            cost = 0
                        
                        exit_time = t + cost
                        vehicle.setExit(exit_time)
                        last_exit_time[direction] = exit_time #update the last_exit_time of the most recent vehicle

                        wait_time = vehicle.getWaitTime()
                        self.wait_times[direction].append(wait_time)
                        
                        
