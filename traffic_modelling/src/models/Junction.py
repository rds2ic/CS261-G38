class Junction:
    def __init__(self, north_traffic : tuple[int, int, int],
                       south_traffic : tuple[int, int, int],
                       east_traffic : tuple[int, int, int],
                       west_traffic : tuple[int, int, int]):
        # tuple[int, int, int] represents the three different directions traffic can flow to
        self.north_traffic = north_traffic
        self.south_traffic = south_traffic
        self.east_traffic = east_traffic
        self.west_traffic = west_traffic

    def configure(self):
        pass