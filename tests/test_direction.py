from src.plaka_sistem.direction import DirectionGate


def test_left_to_right_passes_when_threshold_crossed():
    gate = DirectionGate("left_to_right", enter_line_x=120, exit_line_x=380, min_delta_x=120)
    assert gate.process("t1", 100) is False
    assert gate.process("t1", 240) is False
    assert gate.process("t1", 400) is True


def test_left_to_right_blocks_wrong_direction():
    gate = DirectionGate("left_to_right", enter_line_x=120, exit_line_x=380, min_delta_x=120)
    assert gate.process("t2", 420) is False
    assert gate.process("t2", 320) is False
    assert gate.process("t2", 150) is False


def test_right_to_left_passes_when_threshold_crossed():
    gate = DirectionGate("right_to_left", enter_line_x=380, exit_line_x=120, min_delta_x=120)
    assert gate.process("t3", 420) is False
    assert gate.process("t3", 240) is False
    assert gate.process("t3", 100) is True
