class Junction:
    def __init__(self, north_traffic : tuple[int, int, int],
                       south_traffic : tuple[int, int, int],
                       east_traffic : tuple[int, int, int],
                       west_traffic : tuple[int, int, int],
                       lanes : int,
                       left_turn_lane : bool,
                       bus_cycle_lane : bool,
                       pedestrian_enabled: bool,
                       pedestrian_crossing_time: int,
                       pedestrian_request_interval: int,
                       traffic_priority : str,
                       cycle_length : int,
                       buses_per_hour: int = 0,
                       cycles_per_hour: int = 0):
        # tuple[int, int, int] represents the three different directions traffic can flow to
        self.north_traffic = north_traffic
        self.south_traffic = south_traffic
        self.east_traffic = east_traffic
        self.west_traffic = west_traffic
        self.lanes = lanes
        self.left_turn_lane = left_turn_lane
        self.bus_cycle_lane = bus_cycle_lane

        self.pedestrian_enabled = pedestrian_enabled
        self.pedestrian_crossing_time = pedestrian_crossing_time
        self.pedestrian_request_interval = pedestrian_request_interval

        self.traffic_priority = traffic_priority
        self.cycle_length = cycle_length
        self.buses_per_hour = buses_per_hour
        self.cycles_per_hour = cycles_per_hour

class JunctionBuilder:
    def __init__(self):
        # Default parameters can be set here if needed
        self.north_traffic = (0, 0, 0)
        self.south_traffic = (0, 0, 0)
        self.east_traffic = (0, 0, 0)
        self.west_traffic = (0, 0, 0)
        self.lanes = {'north': 2, 'south': 2, 'east': 2, 'west': 2}  # Example default lane setup
        self.left_turn_lane = False
        self.bus_cycle_lane = False  
        self.pedestrian_enabled = False
        self.pedestrian_crossing_time = 0
        self.pedestrian_request_interval = 0
        self.traffic_priority = {'north': 0, 'south': 0, 'east': 0, 'west': 0}  # Default priorities
        self.cycle_length = 10
        self.buses_per_hour = 0
        self.cycles_per_hour = 0

    def set_traffic(self, north_traffic, south_traffic, east_traffic, west_traffic):
        for traffic in [north_traffic, south_traffic, east_traffic, west_traffic]:
            if any(value < 0 for value in traffic):
                raise ValueError("Traffic values must be non-negative")
            if any(value > 10000 for value in traffic):  #assume 10000 as a upper limit (realistically)
                raise ValueError("Traffic values exceed realistic limits")
        self.north_traffic = north_traffic
        self.south_traffic = south_traffic
        self.east_traffic = east_traffic
        self.west_traffic = west_traffic
        return self

    def set_lanes(self, lanes):
        # validate that lane values are positive integers
        if not all(isinstance(value, int) and value > 0 for value in lanes.values()):
            raise ValueError("Number of lanes must be positive")
        self.lanes = lanes
        return self

    def set_left_turn_lane(self, enabled):
        self.left_turn_lane = enabled
        return self

    def set_bus_cycle_lane(self, lane_type):
        self.bus_cycle_lane = lane_type
        return self

    def set_pedestrian_crossing(self, enabled, crossing_time, requests_interval):
        self.pedestrian_enabled = enabled
        self.pedestrian_crossing_time = crossing_time
        self.pedestrian_request_interval = requests_interval
        return self

    def set_traffic_priority(self, priority):
        self.traffic_priority = priority
        return self

    def set_traffic_priority(self, priority):
        self.traffic_priority = priority
        return self
    
    def set_cycle_length(self, cycle_length):
        if cycle_length <= 0:
            raise ValueError("Cycle length must be positive")
        self.cycle_length = cycle_length
        return self
    
    def set_bus_cycle_lane(self, enabled: bool):
        self.bus_cycle_lane = enabled
        return self

    def set_bus_and_cycle_flow(self, buses_per_hour: int, cycles_per_hour: int):
        self.buses_per_hour = buses_per_hour
        self.cycles_per_hour = cycles_per_hour
        return self

    def build(self):
        return Junction(self.north_traffic, self.south_traffic, self.east_traffic, self.west_traffic,
                        self.lanes, self.left_turn_lane, self.bus_cycle_lane,
                        self.pedestrian_enabled, self.pedestrian_crossing_time, self.pedestrian_request_interval, self.traffic_priority, self.cycle_length, self.buses_per_hour, self.cycles_per_hour)
