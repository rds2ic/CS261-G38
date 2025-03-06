class Junction:
    def __init__(self, north_traffic : tuple[int, int, int],
                       south_traffic : tuple[int, int, int],
                       east_traffic : tuple[int, int, int],
                       west_traffic : tuple[int, int, int],
                       lanes : int,
                       left_turn_lane : bool,
                       bus_cycle_lane : bool,
                       pedestrian_crossing : bool,
                       traffic_priority : str,
                       cycle_length : int):
        # tuple[int, int, int] represents the three different directions traffic can flow to
        self.north_traffic = north_traffic
        self.south_traffic = south_traffic
        self.east_traffic = east_traffic
        self.west_traffic = west_traffic

        self.lanes = lanes
        self.left_turn_lane = left_turn_lane
        self.bus_cycle_lane = bus_cycle_lane
        self.pedestrian_crossing = pedestrian_crossing
        self.traffic_priority = traffic_priority
        self.cycle_length = cycle_length

class JunctionBuilder:
    def __init__(self):
        # Default parameters can be set here if needed
        self.north_traffic = (0, 0, 0)
        self.south_traffic = (0, 0, 0)
        self.east_traffic = (0, 0, 0)
        self.west_traffic = (0, 0, 0)
        self.lanes = {'north': 2, 'south': 2, 'east': 2, 'west': 2}  # Example default lane setup
        self.left_turn_lane = False
        self.bus_cycle_lane = None  # Can be 'bus', 'cycle', or None
        self.pedestrian_crossing = {'enabled': False, 'duration': 0, 'requests_per_hour': 0}
        self.traffic_priority = {'north': 0, 'south': 0, 'east': 0, 'west': 0}  # Default priorities
        self.cycle_length = 10

    def set_traffic(self, north_traffic, south_traffic, east_traffic, west_traffic):
        self.north_traffic = north_traffic
        self.south_traffic = south_traffic
        self.east_traffic = east_traffic
        self.west_traffic = west_traffic
        return self

    def set_lanes(self, lanes):
        self.lanes = lanes
        return self

    def set_left_turn_lane(self, enabled):
        self.left_turn_lane = enabled
        return self

    def set_bus_cycle_lane(self, lane_type):
        self.bus_cycle_lane = lane_type
        return self

    def set_pedestrian_crossing(self, enabled, duration, requests_per_hour):
        self.pedestrian_crossing = {'enabled': enabled, 'duration': duration, 'requests_per_hour': requests_per_hour}
        return self

    def set_traffic_priority(self, priority):
        self.traffic_priority = priority
        return self
    
    def set_cycle_length(self, cycle_length):
        self.cycle_length = cycle_length
        return self

    def build(self):
        return Junction(self.north_traffic, self.south_traffic, self.east_traffic, self.west_traffic,
                        self.lanes, self.left_turn_lane, self.bus_cycle_lane,
                        self.pedestrian_crossing, self.traffic_priority, self.cycle_length)
