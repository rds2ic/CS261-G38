from models import Junction, Vehicle, PedestrianCrossing, BusCycleLane
import random


class Simulation:
    def __init__(self, junction : Junction, pedestrian_crossing : PedestrianCrossing = None, bus_cycle_lane : BusCycleLane = None, simulation_duration : int = 3600):
        self.time = 0           # Time in seconds
        self.cycle_length = junction.cycle_length  # Length of a cycle in seconds
        self.junction = junction # Junction config to be used
        self.simulation_duration = simulation_duration # Duration of the simulation in seconds
        self.pedestrian_crossing = pedestrian_crossing # Pedestrian crossing config to be used
        self.bus_cycle_lane = bus_cycle_lane 

        # Queues for each approach and movement
        self.queues = {
            'north': [],
            'south': [],
            'east': [],
            'west': []
        }
            
        self.left_turn_queues = {
            'north': [],
            'south': [],
            'east': [],
            'west': []
        }
               
        self.bus_queue = []
        self.cycle_queue = []
               
        # Record wait times per direction.
        self.wait_times = {
            'north': [],
            'south': [],
            'east': [],
            'west': []
        }
        
        self.bus_wait_times = []
        self.cycle_wait_times = []

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
        
        self.bus_cycle_lane.configureLane()
        bus_interval = self.bus_cycle_lane.bus_interval
        cycle_interval = self.bus_cycle_lane.cycle_interval
        next_bus_arrival = self.bus_cycle_lane.next_bus_arrival
        next_cycle_arrival = self.bus_cycle_lane.next_cycle_arrival
        

        self.bus_wait_times = []
        self.cycle_wait_times = []

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
        
        last_bus_exit_time = 0

        # Main simulation loop
        for t in range(self.simulation_duration):
            self.time = t

            for direction in ["north", "south", "east", "west"]:
                interval = arrival_intervals[direction]
                if interval is None:
                    continue

                while next_arrivals[direction] is not None and next_arrivals[direction] <= t:
                    
                    movements = ["left", "right","straight"]  
                    movement = random.choice(movements)
                    
                    car = Vehicle(t, movement, vehicle_type="car")
                    
                    if self.junction.left_turn_lane and car.movement == "left":
                        self.left_turn_queues[direction].append(car)
                    else:
                        self.queues[direction].append(car)

                    # Schedule next arrival
                    next_arrivals[direction] += interval
                
                # Sort queue by arrival time
                self.queues[direction].sort(key=lambda v: v.entry)

                # Updae the maximum queue length
                self.max_queue_lengths[direction] = max(self.max_queue_lengths[direction], len(self.queues[direction]))
                
                
            #generate bus arrivals
            if bus_interval is not None and next_bus_arrival is not None:
                while next_bus_arrival <= t:
                    new_bus = Vehicle(entry=t, movement = "straight", vehicle_type="bus")
                    self.bus_queue.append(new_bus)
                    next_bus_arrival += bus_interval

            #generate bike arrivals
            if cycle_interval is not None and next_cycle_arrival is not None:
                while next_cycle_arrival <= t:
                    new_cycle = Vehicle(entry=t, movement = "straight", vehicle_type="cycle")
                    self.cycle_queue.append(new_cycle)
                    next_cycle_arrival += cycle_interval

            # Pedestrian crossing request Every x Seconds
            if self.pedestrian_crossing != None:
                if t % self.pedestrian_crossing.get_request_interval() == 0:
                    self.pedestrian_crossing.pushButton()
                
                self.pedestrian_crossing.update(t)
                
                # Block all traffic during pedestrian crossing
                if self.pedestrian_crossing.is_active():
                    continue 
            
            phase_time = t % self.cycle_length
            if phase_time < (self.cycle_length / 2):
                active_phase = ["north", "south"]
            else:
                active_phase = ["east", "west"]
            
            # Process the active phase (normal lanes)
            for direction in active_phase:
                if self.queues[direction]:
                    vehicle = self.queues[direction][0]  
                    
                    if last_exit_time[direction] == 0:
                        reaction_time = first_reaction_cost
                    else:
                        reaction_time = gap_reaction_cost

                    if t >= last_exit_time[direction] + reaction_time:
                        vehicle = self.queues[direction].pop(0)\
                            
                        
                        if vehicle.exit == "right":
                            cost = right_turn_cost
                        elif vehicle.exit == "left":
                            cost = left_turn_cost
                        else:
                            cost = 0
                        
                        exit_time = t + cost
                        vehicle.setExit(exit_time)
                        last_exit_time[direction] = exit_time #update the last_exit_time of the most recent vehicle

                        wait_time = vehicle.getWaitTime()
                        self.wait_times[direction].append(wait_time)
                
                if self.bus_cycle_lane.busesPerHour > 0: 
                    if self.bus_queue:
                        bus = self.bus_queue[0]
                        if last_bus_exit_time == 0:
                            reaction_time = first_reaction_cost
                        else:
                            reaction_time = gap_reaction_cost
                        if t >= last_bus_exit_time + reaction_time:
                            bus = self.bus_queue.pop(0)
                            exit_time = t + 2    #buses are slower
                            bus.setExit(exit_time)
                            last_bus_exit_time = exit_time
                            print("ahahah")
                        wait_time = bus.getWaitTime()
                        if wait_time is not None:
                            self.bus_wait_times.append(wait_time)
                            self.wait_times[direction].append(wait_time)
                            
                    if self.cycle_queue:
                        cycle = self.cycle_queue.pop(0)
                        exit_time = t + 0.5
                        cycle.setExit(exit_time)
                        
            #active phase for left turn queues                   
            for direction in active_phase:
                if self.junction.left_turn_lane and self.left_turn_queues[direction]:
                    vehicle = self.left_turn_queues[direction][0]  
                    
                    if last_exit_time[direction] == 0:
                        reaction_time = first_reaction_cost
                    else:
                        reaction_time = gap_reaction_cost

                    if t >= last_exit_time[direction] + reaction_time:                    
                        self.left_turn_queues[direction].pop(0)
                        
                        cost = left_turn_cost *0.3
                        
                        exit_time = t + cost
                        vehicle.setExit(exit_time)
                        last_exit_time[direction] = exit_time #update the last_exit_time of the most recent vehicle

                        wait_time = vehicle.getWaitTime()
                        self.wait_times[direction].append(wait_time)
                        



