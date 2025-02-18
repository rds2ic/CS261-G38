class Simuluation:
    def __init__(self):
        self.time = 0           # Time in seconds
        self.cycle_length = 10  # Length of a cycle in seconds
    
    def runSiumulation(self):
        pass

    def calculateWaitTimes(self):
        pass

    def calculateQueueLengths(self):
        pass

    def getActivePhase(self):
        """ Returns the active phase of the traffic light """
        return self.time % self.cycle_length

    def getInput(self, input):
        pass