import pytest
from simulation import Simulation, StatsCollector
from models.Junction import Junction, JunctionBuilder

def test_queue_length_calculation():
    #arrange
    junction = (JunctionBuilder()
                .set_traffic(north_traffic=(10, 5, 5),
                             south_traffic=(8, 4, 4),
                             east_traffic=(7, 6, 6),
                             west_traffic=(9, 5, 5))
                .build())

    sim = Simulation(junction, simulation_duration=3600)
    sim.runSimulation()
    
    stats = StatsCollector(sim)

    #act
    max_queues = stats.getMaxQueueLengths()

    #assert
    assert max_queues['north'] >= 0
    assert max_queues['south'] >= 0
    assert max_queues['east'] >= 0
    assert max_queues['west'] >= 0
