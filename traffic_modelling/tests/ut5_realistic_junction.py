import pytest
from models.Junction import JunctionBuilder

def test_realistic_junction():
    junction = (JunctionBuilder()
                .set_traffic(north_traffic=(10, 5, 5),
                             south_traffic=(8, 4, 4),
                             east_traffic=(7, 6, 6),
                             west_traffic=(9, 5, 5))
                .build())

    # ensure that all lanes do not exceed capacity
    assert sum(junction.north_traffic) <= 20, "North traffic exceeds lane capacity"
    assert sum(junction.south_traffic) <= 20, "South traffic exceeds lane capacity"
    assert sum(junction.east_traffic) <= 20, "East traffic exceeds lane capacity"
    assert sum(junction.west_traffic) <= 20, "West traffic exceeds lane capacity"

    #ensure cycle length is positive
    assert junction.cycle_length > 0, "Cycle length must be positive"

    #validate lane count
    for lanes in junction.lanes.values():
        assert lanes > 0, "Number of lanes must be positive"
