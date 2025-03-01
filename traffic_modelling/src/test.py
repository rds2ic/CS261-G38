from models import Junction
from simulation import Simulation
from simulation import StatsCollector

if __name__ == '__main__':
    # Create a Junction instance with the given traffic flows.
    # Each tuple is (straight, right, left) vehicles per hour.
    junction = Junction(
        north_traffic=(200, 50, 50),   # Example: total 300 vph for north
        south_traffic=(150, 50, 50),      # total 250 vph for south
        east_traffic=(50, 50, 50),        # total 150 vph for east
        west_traffic=(50, 25, 25)         # total 100 vph for west
    )

    # Create a Simulation instance for 1 hour (3600 seconds)
    sim = Simulation(junction, simulation_duration=3600)
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
