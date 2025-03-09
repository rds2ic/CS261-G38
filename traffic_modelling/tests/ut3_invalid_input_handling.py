import pytest
from models.Junction import JunctionBuilder

def test_invalid_input_handling():
    #test for negative traffic values
    with pytest.raises(ValueError, match="Traffic values must be non-negative"):
        JunctionBuilder().set_traffic(
            north_traffic=(-5, 0, 0), 
            south_traffic=(0, 0, 0), 
            east_traffic=(0, 0, 0), 
            west_traffic=(0, 0, 0)
        ).build()

    #test for unrealistic large traffic values
    with pytest.raises(ValueError, match="Traffic values exceed realistic limits"):
        JunctionBuilder().set_traffic(
            north_traffic=(1000000, 0, 0), 
            south_traffic=(0, 0, 0), 
            east_traffic=(0, 0, 0), 
            west_traffic=(0, 0, 0)
        ).build()

    #test for missing value
    with pytest.raises(ValueError, match=r"Traffic value missing"):
        (JunctionBuilder()
            .set_traffic(north_traffic=( 600, 300), # Missing value
                         south_traffic=(150, 250, 350),
                         east_traffic=(50, 100, 150),
                         west_traffic=(75, 125, 175))
            .build())
        
    #test for non integer value
    with pytest.raises(ValueError, match=r"Traffic values must be an integer"):
        (JunctionBuilder()
            .set_traffic(north_traffic=(100, "600", 300), # Non integer value
                         south_traffic=(150, 250, 350),
                         east_traffic=(50, 100, 150),
                         west_traffic=(75, 125, 175))
            .build())

    #test for a negative crossing_time 
    with pytest.raises(ValueError, match=r"Pedestrian Crossing values must be greater than 0"):
        (JunctionBuilder()
            .set_traffic(north_traffic=(0, 0, 0), 
                         south_traffic=(0, 0, 0), 
                         east_traffic=(0, 0, 0),
                         west_traffic=(0, 0, 0))
            .set_pedestrian_crossing(True, -5, 20)  # Invalid: duration < 0
            .build())
    
    #test for a negative requests_interval 
    with pytest.raises(ValueError, match=r"Pedestrian Crossing values must be greater than 0"):
        (JunctionBuilder()
            .set_traffic(north_traffic=(0, 0, 0), 
                         south_traffic=(0, 0, 0), 
                         east_traffic=(0, 0, 0),
                         west_traffic=(0, 0, 0))
            .set_pedestrian_crossing(True, 5, -20)  # Invalid: duration < 0
            .build())
    
    #test for a non integer crossing_time 
    with pytest.raises(ValueError, match=r"Pedestrian Crossing values must be an integer"):
        (JunctionBuilder()
            .set_traffic(north_traffic=(0, 0, 0), 
                         south_traffic=(0, 0, 0), 
                         east_traffic=(0, 0, 0),
                         west_traffic=(0, 0, 0))
            .set_pedestrian_crossing(True, "-5", 20)  # Invalid: duration < 0
            .build())
    
    #test for a non integer requests_interval 
    with pytest.raises(ValueError, match=r"Pedestrian Crossing values must be an integer"):
        (JunctionBuilder()
            .set_traffic(north_traffic=(0, 0, 0), 
                         south_traffic=(0, 0, 0), 
                         east_traffic=(0, 0, 0),
                         west_traffic=(0, 0, 0))
            .set_pedestrian_crossing(True, "-5", 20)  # Invalid: duration < 0
            .build())
    
    #test for invalid lane configuration (such as negative lanes)
    with pytest.raises(ValueError, match="Number of lanes must be positive"):
        JunctionBuilder().set_lanes({'north': -1, 'south': 2, 'east': 2, 'west': 2}).build()

    #test for invalid cycle length (such as negative or zero)
    with pytest.raises(ValueError, match="Cycle length must be positive"):
        JunctionBuilder().set_cycle_length(-10).build()
