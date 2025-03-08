class BusCycleLane:
    def __init__(self, busesPerHour : int, cyclesPerHour : int):
        self.busesPerHour = busesPerHour
        self.cyclesPerHour = cyclesPerHour
    
        self.bus_interval = None
        self.cycle_interval = None
        
        self.next_bus_arrival = None
        self.next_cycle_arrival = None
        
    def configureLane(self):
        #if busesperhour is 0 then no buses arrive
        if self.busesPerHour > 0:
            self.bus_interval = 3600 / self.busesPerHour
            self.next_bus_arrival = 0
        else:
            self.bus_interval = None
            self.next_bus_arrival = None
        
        if self.cyclesPerHour > 0:
            self.cycle_interval = 3600 / self.cyclesPerHour
            self.next_cycle_arrival = 0
        else:
            self.cycle_interval = None
            self.next_cycle_arrival = None