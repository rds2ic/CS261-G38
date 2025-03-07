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

    #test for invalid lane configuration (such as negative lanes)
    with pytest.raises(ValueError, match="Number of lanes must be positive"):
        JunctionBuilder().set_lanes({'north': -1, 'south': 2, 'east': 2, 'west': 2}).build()

    #test for invalid cycle length (such as negative or zero)
    with pytest.raises(ValueError, match="Cycle length must be positive"):
        JunctionBuilder().set_cycle_length(-10).build()
