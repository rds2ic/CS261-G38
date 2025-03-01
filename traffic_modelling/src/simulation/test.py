from simulation import Simulation
from models import Junction

""" Test program """

# Create a Junction instance with the given traffic flows.
# Each tuple is (straight, right, left) in vehicles per hour.
junction = Junction(
    north_traffic=(2000, 50, 50),   # Total 300 vph
    south_traffic=(150, 50, 50),   # Total 250 vph
    east_traffic=(50, 50, 50),     # Total 150 vph
    west_traffic=(50, 25, 25)      # Total 100 vph
)

# Create a Simulation instance with a 1-hour duration (3600 seconds).
sim = Simulation(junction, simulation_duration=3600)

# Run the simulation.
sim.runSimulation()

# Calculate and print the output statistics.
avg_wait = sim.calculateAverageWaitTime()
max_wait = sim.calculateMaxWaitTimes()
max_queues = sim.getMaxQueueLengths()

print("Average Wait Times (seconds):", avg_wait)
print("Maximum Wait Times (seconds):", max_wait)
print("Maximum Queue Lengths:", max_queues)