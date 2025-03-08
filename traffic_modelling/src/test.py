from models import Junction, JunctionBuilder, PedestrianCrossing, BusCycleLane
from simulation import Simulation
from simulation import StatsCollector



def run_simulation(north_traffic, south_traffic, east_traffic, west_traffic, lanes, left_turn_lane, bus_cycle_lane, pedestrian_crossing, simulation_duration=3600, buses_per_hour=0,
        cycles_per_hour=0):
                
        crossing_time = 7
        requests_interval = 60

        junction = (JunctionBuilder()
                .set_traffic(north_traffic, south_traffic, east_traffic, west_traffic)
                .set_lanes(lanes)
                .set_left_turn_lane(left_turn_lane)
                .set_bus_cycle_lane(bus_cycle_lane)
                .set_bus_and_cycle_flow(buses_per_hour, cycles_per_hour)
                .set_pedestrian_crossing(enabled=pedestrian_crossing, crossing_time=crossing_time, requests_interval=requests_interval)
                .build())
        


        # Create a Simulation instance for 1 hour (3600 seconds)
        sim = Simulation(junction, simulation_duration=simulation_duration)
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
        "lanes": 3, "left_turn_lane": False, "bus_cycle_lane": True, "pedestrian_crossing": False, "simulation_duration": 3600, 
        "buses_per_hour": 10, "cycles_per_hour": 20 },

        {"north_traffic": (200, 50, 50), "south_traffic": (1500, 500, 500),
        "east_traffic": (50, 50, 50), "west_traffic": (100, 50, 50),
        "lanes": 3, "left_turn_lane": False, "bus_cycle_lane": False, "pedestrian_crossing": False, "simulation_duration": 3600},

        {"north_traffic": (200, 50, 50), "south_traffic": (1500, 500, 500),
        "east_traffic": (50, 50, 50), "west_traffic": (100, 50, 50),
        "lanes": 3, "left_turn_lane": False, "bus_cycle_lane": False, "pedestrian_crossing": True, "simulation_duration": 3600}]

        results = []
        for i, scenario in enumerate(scenarios):
                print(f"\nScenario {i+1}\n")
                result = run_simulation(**scenario)
                results.append(result)
