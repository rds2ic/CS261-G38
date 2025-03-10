from models import JunctionBuilder, Vehicle, PedestrianCrossing
from simulation import Simulation, StatsCollector

def test_north_vehicle_arrival():
    # Test that vehicles arrive from the north direction correctly
    junction = (JunctionBuilder()
            .set_traffic(north_traffic=(100, 100, 100), 
                        south_traffic=(0, 0, 0), 
                        east_traffic=(0, 0, 0),
                        west_traffic=(0, 0, 0))
            .build())
    sim = Simulation(junction, simulation_duration=1) # Set simulation duration to 1 so that vehicles do not have time to leave
    sim.runSimulation()

    assert len(sim.queues['north']) > 0  # Vehicles should arrive at the north queue
    assert len(sim.queues['south']) == 0  # No vehicles on the south
    assert len(sim.queues['east']) == 0  # No vehicles on the east
    assert len(sim.queues['west']) == 0  # No vehicles on the west

def test_south_vehicle_arrival():
    # Test that vehicles arrive from the south direction correctly
    junction = (JunctionBuilder()
            .set_traffic(north_traffic=(0, 0, 0), 
                        south_traffic=(100, 100, 100), 
                        east_traffic=(0, 0, 0),
                        west_traffic=(0, 0, 0))
            .build())
    sim = Simulation(junction, simulation_duration=1) # Set simulation duration to 1 so that vehicles do not have time to leave
    sim.runSimulation()

    assert len(sim.queues['north']) == 0  # No vehicles on the north
    assert len(sim.queues['south']) > 0  # Vehicles should arrive at the south queue
    assert len(sim.queues['east']) == 0  # No vehicles on the east
    assert len(sim.queues['west']) == 0  # No vehicles on the west

def test_east_vehicle_arrival():
    # Test that vehicles arrive from the east direction correctly
    junction = (JunctionBuilder()
            .set_traffic(north_traffic=(0, 0, 0), 
                        south_traffic=(0, 0, 0), 
                        east_traffic=(100, 100, 100),
                        west_traffic=(0, 0, 0))
            .build())
    sim = Simulation(junction, simulation_duration=1) # Set simulation duration to 1 so that vehicles do not have time to leave
    sim.runSimulation()

    assert len(sim.queues['north']) == 0  # No vehicles on the north
    assert len(sim.queues['south']) == 0  # No vehicles on the south
    assert len(sim.queues['east']) > 0  # Vehicles should arrive at the east queue
    assert len(sim.queues['west']) == 0  # No vehicles on the west

def test_west_vehicle_arrival():
    # Test that vehicles arrive from the west direction correctly
    junction = (JunctionBuilder()
            .set_traffic(north_traffic=(0, 0, 0), 
                        south_traffic=(0, 0, 0), 
                        east_traffic=(0, 0, 0),
                        west_traffic=(100, 100, 100))
            .build())
    sim = Simulation(junction, simulation_duration=1) # Set simulation duration to 1 so that vehicles do not have time to leave
    sim.runSimulation()

    assert len(sim.queues['north']) == 0  # No vehicles on the north
    assert len(sim.queues['south']) == 0  # No vehicles on the south
    assert len(sim.queues['east']) == 0  # No vehicles on the east
    assert len(sim.queues['west']) > 0  # Vehicles should arrive at the west queue

def test_zero_vehicle_arrival():
    # Test that no vehicles arrive at each direction
    junction = (JunctionBuilder()
            .set_traffic(north_traffic=(0, 0, 0), 
                        south_traffic=(0, 0, 0), 
                        east_traffic=(0, 0, 0),
                        west_traffic=(0, 0, 0))
            .build())
    sim = Simulation(junction, simulation_duration=18000) 
    sim.runSimulation()

    stats = StatsCollector(sim)
    avg_wait = stats.calculateAverageWaitTime()
    max_wait = stats.calculateMaxWaitTimes()
    max_queues = stats.getMaxQueueLengths()
    
    # Ensure no vehicles are in any queue 
    # Ensure all average and maximum wait times are None
    # Ensure max queue length is 0
    for direction in sim.queues:
        assert len(sim.queues[direction]) == 0
        assert avg_wait[direction] == None
        assert max_wait[direction] == None
        assert max_queues[direction] == 0

def test_equal_stats():
    # Test that opposing lanes have the same stats for the same traffic values
    junction = (JunctionBuilder()
            .set_traffic(north_traffic=(200, 200, 200), 
                        south_traffic=(200, 200, 200), 
                        east_traffic=(100, 100, 100),
                        west_traffic=(100, 100, 100))
            .build())
    sim = Simulation(junction, simulation_duration=18000) 
    sim.runSimulation()

    
    stats = StatsCollector(sim)
    avg_wait = stats.calculateAverageWaitTime()
    max_wait = stats.calculateMaxWaitTimes()
    max_queues = stats.getMaxQueueLengths()

    # Verify that the opposing lanes have the same average wait time, max wait time, and queue lengths
    assert avg_wait['north'] == avg_wait['south']
    assert avg_wait['east'] == avg_wait['west']

    assert max_wait['north'] == max_wait['south']
    assert max_wait['east'] == max_wait['west']

    assert max_queues['north'] == max_queues['south']
    assert max_queues['east'] == max_queues['west']

    

def test_different_avg_wait():
    # Test if different traffic values result in different average wait times
    junction = (JunctionBuilder()
            .set_traffic(north_traffic=(100, 200, 300), 
                        south_traffic=(400, 250, 150), 
                        east_traffic=(200, 100, 400),
                        west_traffic=(300, 400, 200))
            .build())
    sim = Simulation(junction, simulation_duration=18000) 
    sim.runSimulation()

    stats = StatsCollector(sim)
    avg_wait = stats.calculateAverageWaitTime()
    
    # Ensure all average wait times are different
    assert avg_wait['north'] != avg_wait['south']
    assert avg_wait['north'] != avg_wait['east']
    assert avg_wait['north'] != avg_wait['west']
    assert avg_wait['south'] != avg_wait['east']
    assert avg_wait['south'] != avg_wait['west']
    assert avg_wait['south'] != avg_wait['west']


def test_pedestrian_simulation():
    # Test that for the same traffic values junctions with crossings have longer average wait times than junctions without
    junction1 = (JunctionBuilder()
            .set_traffic(north_traffic=(100, 200, 300), 
                        south_traffic=(400, 250, 150), 
                        east_traffic=(200, 100, 400),
                        west_traffic=(150, 250, 200))
            .set_pedestrian_crossing(False, 10, 10)
            .build())
    sim1 = Simulation(junction1, simulation_duration=18000) 
    sim1.runSimulation()

    junction2 = (JunctionBuilder()
            .set_traffic(north_traffic=(100, 200, 300), 
                        south_traffic=(400, 250, 150), 
                        east_traffic=(200, 100, 400),
                        west_traffic=(150, 250, 200))
            .set_pedestrian_crossing(True, 10, 60)
            .build())
    sim2 = Simulation(junction2, simulation_duration=18000) 
    sim2.runSimulation()

    stats1 = StatsCollector(sim1)
    stats2 = StatsCollector(sim2)

    avg_wait1 = stats1.calculateAverageWaitTime()
    avg_wait2 = stats2.calculateAverageWaitTime()

    # Verify that junctions with pedestrian crossings have longer wait times
    assert avg_wait1['north'] <= avg_wait2['north']
    assert avg_wait1['south'] <= avg_wait2['south']
    assert avg_wait1['east'] <= avg_wait2['east']
    assert avg_wait1['west'] <= avg_wait2['west']

    

def test_pedestrian_duration_simulation():
    # Tests that for the same traffic values junctions the junction with the longer crossing duration will have a longer average wait time 
    junction1 = (JunctionBuilder()
            .set_traffic(north_traffic=(100, 200, 300), 
                        south_traffic=(200, 250, 150), 
                        east_traffic=(200, 100, 250),
                        west_traffic=(150, 250, 200))
            .set_pedestrian_crossing(True, 12, 45)
            .build())
    sim1 = Simulation(junction1, simulation_duration=18000) 
    sim1.runSimulation()

    junction2 = (JunctionBuilder()
            .set_traffic(north_traffic=(100, 200, 300), 
                        south_traffic=(200, 250, 150), 
                        east_traffic=(200, 100, 250),
                        west_traffic=(150, 250, 200))
            .set_pedestrian_crossing(True, 6, 45)
            .build())
    sim2 = Simulation(junction2, simulation_duration=18000) 
    sim2.runSimulation()

    stats1 = StatsCollector(sim1)
    stats2 = StatsCollector(sim2)

    avg_wait1 = stats1.calculateAverageWaitTime()
    avg_wait2 = stats2.calculateAverageWaitTime()

    # Ensure that longer pedestrian crossing duration leads to longer vehicle wait times
    assert avg_wait1['north'] > avg_wait2['north']
    assert avg_wait1['south'] > avg_wait2['south']
    assert avg_wait1['east'] > avg_wait2['east']
    assert avg_wait1['west'] > avg_wait2['west']
