class Vehicle:
    def __init__(self, entry : int, movement : str, vehicle_type: str = "car", exit : int=None):
        self.entry = entry
        self.exit = exit
        self.time = 0
        self.movement = movement # "straight", "right", or "left"
        self.vehicle_type = vehicle_type
        
    def getEntry(self):
        return self.entry
    
    def setExit(self, exit : int):
        self.exit = exit
    
    def getExit(self):
        return self.exit
    
    def getWaitTime(self):
        return self.exit - self.entry if self.exit is not None else None

    def getVehicleType(self):
        return self.vehicle_type