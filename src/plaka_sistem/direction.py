from dataclasses import dataclass


@dataclass
class TrackState:
    first_x: float
    last_x: float
    passed: bool = False


class DirectionGate:
    def __init__(self, allowed_direction: str, enter_line_x: int, exit_line_x: int, min_delta_x: int):
        if allowed_direction not in {"left_to_right", "right_to_left"}:
            raise ValueError("allowed_direction must be 'left_to_right' or 'right_to_left'")
        self.allowed_direction = allowed_direction
        self.enter_line_x = enter_line_x
        self.exit_line_x = exit_line_x
        self.min_delta_x = min_delta_x
        self._tracks: dict[str, TrackState] = {}

    def process(self, track_id: str, centroid_x: float) -> bool:
        state = self._tracks.get(track_id)
        if state is None:
            self._tracks[track_id] = TrackState(first_x=centroid_x, last_x=centroid_x)
            return False

        state.last_x = centroid_x
        if state.passed:
            return True

        delta = state.last_x - state.first_x

        if self.allowed_direction == "left_to_right":
            passed = (
                state.first_x <= self.enter_line_x
                and state.last_x >= self.exit_line_x
                and delta >= self.min_delta_x
            )
        else:
            passed = (
                state.first_x >= self.enter_line_x
                and state.last_x <= self.exit_line_x
                and -delta >= self.min_delta_x
            )

        if passed:
            state.passed = True
        return passed
