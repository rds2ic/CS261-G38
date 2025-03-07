class PedestrianCrossing:
    def __init__(self, crossing_time : int, requests_interval : int):
        self.crossing_time = crossing_time # Duration of the crossing in seconds
        self.requests_interval = requests_interval # Time between pedestrians requesting to cross
        self.crossing_active = False # Crossing status
        self.request = False # Pedestrian crossing request status
        self.crossing_start = None # Time the crossing begins
        self.max_green_timer = 30 # Max duration  


    def pushButton(self):
        # Pedestrian presses the button to request crossing
        self.request = True

    

    def update(self, time):
        # Ensures the duration of the crossing is correct
        if self.crossing_active:
            if time >= self.crossing_start + self.crossing_time:
                self.crossing_active = False
                self.crossing_start = None
            return
        
        # Updates the timer for green light
        if self.request:
            self.max_green_timer -= 1
        
        # Checks to see if all the conditions to begin crossing are true
        if not self.crossing_active and self.request and self.max_green_timer <= 0:
            self.crossing_active = True
            self.crossing_start = time
            self.request = False
            self.max_green_timer = 30

    def get_request_interval(self):
        # Returns the request interval
        return self.requests_interval

    def is_active(self):
        # Returns True if crossing is active
        return self.crossing_active
    
