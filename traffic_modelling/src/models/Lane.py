class Lane:
    def __init__(self, lane_count : int):
        self.lane_count = lane_count
    
    def getLaneCount(self):
        return self.lane_count
    
    def setLaneCount(self, lane_count : int):
        self.lane_count = lane_count

    def manageLaneFlow(self):
        pass