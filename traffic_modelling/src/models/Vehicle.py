class Vehicle:
    def __init__(self, entry, exit):
        self.entry = entry
        self.exit = exit
    
    def getEntry(self):
        return self.entry
    
    def getExit(self):
        return self.exit
    
    def getWaitTime(self):
        return self.exit - self.entry