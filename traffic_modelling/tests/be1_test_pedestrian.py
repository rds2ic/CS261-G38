import pytest
from models import PedestrianCrossing

def test_push_button():
    # Test that crossing is requested correctly
    crossing = PedestrianCrossing(10, 25)
    assert not crossing.request  # Request should be False at start
    
    crossing.pushButton()
    assert crossing.request      # Button press should set request to True


def test_crossing_activation():
    # Test that crossing activates correctly
    crossing = PedestrianCrossing(10, 25)
    crossing.pushButton()
    timer = crossing.max_green_timer

    # Crossing shouldn't be active until max green timer is 0
    for t in range (0, timer):
        assert not crossing.is_active() 
        crossing.update(t)
        
        
    assert crossing.is_active()  # Crossing should be active


def test_crossing_duration():
    # Test that crossing is active for the correct duration
    crossing = PedestrianCrossing(10, 25)
    crossing.pushButton()
    timer = crossing.max_green_timer

    
    for t in range (1, timer+10): 
        crossing.update(t)

        # Crossing shouldn't be active until max green timer is 0
        if t >= timer:
            # Check if crossing is active for 10 seconds
            assert crossing.is_active()
    

    crossing.update(timer+10)
    assert not crossing.is_active()  # Crossing should be inactive after 10 seconds

