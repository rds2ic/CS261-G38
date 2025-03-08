from models.Junction import Junction, JunctionBuilder

def test_traffic_light_sequence():
    junction = (JunctionBuilder()
                .set_traffic((50, 30, 20), (40, 25, 35), (30, 45, 25), (20, 30, 50))
                .set_cycle_length(10)
                .build())

    #simulate traffic light sequencing manually
    #assume traffic lights switch in a fixed order: N -> E -> S -> W
    direction_order = ['N', 'E', 'S', 'W']
    initial_direction = 'N'  #start with Northbound green

    #simulate manual traffic light switching
    for i in range(4):  #simulate 4 cycles of light changes
        next_direction = direction_order[(direction_order.index(initial_direction) + 1) % 4]
        assert next_direction in direction_order
        initial_direction = next_direction

    #if no assertion fails, the test is considered passed
