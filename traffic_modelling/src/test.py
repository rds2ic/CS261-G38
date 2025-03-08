from models import Junction, JunctionBuilder, PedestrianCrossing, BusCycleLane
from simulation import Simulation
from simulation import StatsCollector



def run_simulation(north_traffic, south_traffic, east_traffic, west_traffic, lanes, left_turn_lane, bus_cycle_lane, pedestrian_crossing, simulation_duration=3600):
        junction = (JunctionBuilder()
                .set_traffic(north_traffic, south_traffic, east_traffic, west_traffic)
                .set_lanes(lanes)
                .set_left_turn_lane(left_turn_lane)
                .build())
        # Create a PedestrianCrossing instance which has crossings
        # The crossings last 7 seconds and are requested every 60 seconds
        pedestrian_crossing = PedestrianCrossing(7, 60)
        # create buscyclelane instance
        if bus_cycle_lane:
                bc_lane = BusCycleLane(busesPerHour=10, cyclesPerHour=20)
        else:
                bc_lane = BusCycleLane(0, 0)

        # Create a Simulation instance for 1 hour (3600 seconds)
        sim = Simulation(junction, pedestrian_crossing, bc_lane, simulation_duration=simulation_duration)
        sim.runSimulation()

        # Use StatsCollector to compute statistics
        stats = StatsCollector(sim)
        avg_wait = stats.calculateAverageWaitTime()
        max_wait = stats.calculateMaxWaitTimes()
        max_queues = stats.getMaxQueueLengths()
        active_phase = stats.getActivePhase()

        print("Average Wait Times (seconds):", avg_wait)
        print("Maximum Wait Times (seconds):", max_wait)
        print("Maximum Queue Lengths:", max_queues)
        print("Active Phase:", active_phase)



if __name__ == '__main__':
        scenarios = [
        {"north_traffic": (200, 50, 50), "south_traffic": (1500, 500, 500),
        "east_traffic": (50, 50, 50), "west_traffic": (100, 50, 50),
        "lanes": 3, "left_turn_lane": False, "bus_cycle_lane": False, "pedestrian_crossing": False, "simulation_duration": 3600},
        
        {"north_traffic": (200, 50, 50), "south_traffic": (1500, 500, 500),
        "east_traffic": (50, 50, 50), "west_traffic": (100, 50, 50),
        "lanes": 3, "left_turn_lane": True, "bus_cycle_lane": False, "pedestrian_crossing": False, "simulation_duration": 3600},
        
        {"north_traffic": (200, 50, 50), "south_traffic": (1500, 500, 500),
        "east_traffic": (50, 50, 50), "west_traffic": (100, 50, 50),
        "lanes": 3, "left_turn_lane": False, "bus_cycle_lane": False, "pedestrian_crossing": False, "simulation_duration": 3600},
        
        {"north_traffic": (200, 50, 50), "south_traffic": (1500, 500, 500),
        "east_traffic": (50, 50, 50), "west_traffic": (100, 50, 50),
        "lanes": 3, "left_turn_lane": False, "bus_cycle_lane": BusCycleLane(busesPerHour=10, cyclesPerHour=20), "pedestrian_crossing": False, "simulation_duration": 3600},
    ]

        results = []
        for i, scenario in enumerate(scenarios):
                print(f"\nScenario {i+1}\n")
                result = run_simulation(**scenario)
                results.append(result)
