class Simuluation:
    def __init__(self):
        self.time = 0           # Time in seconds
        self.cycle_length = 10  # Length of a cycle in seconds
        self.NS_Light = TrafficLight() # Traffic light for North-South
        self.EW_Light = TrafficLight() # Traffic light for East-West
        self.greenTime = greenTime # Length of green light in seconds
        self.yellowTime = yellowTime # Length of yellow light in seconds
        self.trafficLightTimer = greenTime  # Start with green light for North-South
        self.trafficLightState = "NS_GREEN"  # Start with North-South lights green
        self.previousTrafficState = self.trafficLightState # Set previous state
        self.redPause = 1 # Length of all traffic lights as red
        
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

    def changeLights(self):
        # Changes the traffic lights depending on the traffic light state

        # Checks if the North-South lights are green
        if self.trafficLightState == "NS_GREEN":
            self.NS_Light.setState("GREEN")
            self.EW_Light.setState("RED")

        # Checks if the North-South lights are yellow
        elif self.trafficLightState == "NS_YELLOW":
            self.NS_Light.setState("YELLOW")
            self.EW_Light.setState("RED")

        # Checks if all the lights are red
        elif self.trafficLightState == "ALL_RED":
            self.NS_Light.setState("RED")
            self.EW_Light.setState("RED")
        
        # Checks if the East-West lights are yellow
        elif self.trafficLightState == "EW_YELLOW":
            self.NS_Light.setState("RED")
            self.EW_Light.setState("YELLOW")

        # Checks if the East-West lights are green
        elif self.trafficLightState == "EW_GREEN":
            self.NS_Light.setState("RED")
            self.EW_Light.setState("GREEN")
           

    def updateLights(self):
        # Updates the traffic light states based on a fixed time signal system and that opposite traffice lights are the same

        # Checks if its time to change the lights
        if self.trafficLightTimer <=0:
            
            if self.trafficLightState == "NS_GREEN":
                self.trafficLightState = "NS_YELLOW"
                self.trafficLightTimer = self.yellowTime

            elif self.trafficLightState == "NS_YELLOW" and self.previousTrafficState == "NS_GREEN":
                self.trafficLightState = "ALL_RED"
                self.trafficLightTimer = self.redPause
            
            elif self.trafficLightState == "NS_YELLOW" and self.previousTrafficState == "ALL_RED":
                self.trafficLightState = "NS_GREEN"
                self.trafficLightTimer = self.greenTime
            
            elif self.trafficLightState == "ALL_RED" and self.previousTrafficState == "NS_YELLOW":
                self.trafficLightState = "EW_YELLOW"
                self.trafficLightTimer = self.yellowTime

            elif self.trafficLightState == "ALL_RED" and self.previousTrafficState == "EW_YELLOW":
                self.trafficLightState = "NS_YELLOW"
                self.trafficLightTimer = self.yellowTime

            elif self.trafficLightState == "EW_YELLOW" and self.previousTrafficState == "ALL_RED":
                self.trafficLightState = "EW_GREEN"
                self.trafficLightTimer = self.redPause

            elif self.trafficLightState == "EW_YELLOW" and self.previousTrafficState == "EW_GREEN":
                self.trafficLightState = "ALL_RED"
                self.trafficLightTimer = self.redPause
            
            elif self.trafficLightState == "EW_GREEN":
                self.trafficLightState = "EW_YELLOW"
                self.trafficLightTimer = self.yellowTime

            self.previousTrafficState = self.trafficLightState
            self.changeLights()

        self.trafficLightTimer -= 1 # Decrement traffic light timer
