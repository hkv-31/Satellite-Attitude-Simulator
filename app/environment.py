from dataclasses import dataclass
from .config import (
    ANGLE_MIN, ANGLE_MAX, ANGLE_STEP,
    VELOCITY_MIN, VELOCITY_MAX, VELOCITY_STEP,
    ACTIONS, TARGET_DEFAULT
)

@dataclass
class SatelliteState:
    angle: float
    angular_velocity: float

class SatelliteEnv:
    """Small, deterministic 1D attitude-control simulator."""

    def __init__(self, target_angle: float = TARGET_DEFAULT):
        self.target_angle = float(target_angle)
        self.state = SatelliteState(0.0, 0.0)

    def reset(self, angle: float = 0.0, angular_velocity: float = 0.0):
        self.state = SatelliteState(float(angle), float(angular_velocity))
        return self.state

    def _clamp(self, x, lo, hi):
        return max(lo, min(hi, x))

    def _discretize(self, value, step, lo, hi):
        q = round(value / step) * step
        return int(self._clamp(q, lo, hi))

    def state_key(self):
        return (
            self._discretize(self.state.angle, ANGLE_STEP, ANGLE_MIN, ANGLE_MAX),
            self._discretize(
                self.state.angular_velocity,
                VELOCITY_STEP,
                VELOCITY_MIN,
                VELOCITY_MAX,
            ),
        )

    def step(self, action: int):
        if action not in ACTIONS:
            raise ValueError("action must be -1, 0, or 1")

        # Very simple physics:
        # control changes angular acceleration; damping prevents runaway velocity.
        acceleration = action * 1.5
        new_velocity = self.state.angular_velocity * 0.85 + acceleration
        new_velocity = self._clamp(new_velocity, VELOCITY_MIN, VELOCITY_MAX)

        new_angle = self.state.angle + new_velocity
        new_angle = self._clamp(new_angle, ANGLE_MIN, ANGLE_MAX)

        self.state = SatelliteState(new_angle, new_velocity)

        error = abs(self.target_angle - new_angle)
        reward = -error - 0.15 * abs(new_velocity)

        done = error <= 2.5 and abs(new_velocity) <= 1.0

        if done:
            reward += 100.0

        return self.state, reward, done

    def simulate(self, q_table, start_angle=0.0, start_velocity=0.0, max_steps=100):
        self.reset(start_angle, start_velocity)
        history = []

        for step in range(max_steps):
            state = self.state_key()
            action = max(
                ACTIONS,
                key=lambda a: q_table.get(str(state), {}).get(str(a), 0.0)
            )
            state_after, reward, done = self.step(action)

            history.append({
                "step": step + 1,
                "angle": round(state_after.angle, 4),
                "angular_velocity": round(state_after.angular_velocity, 4),
                "action": action,
                "action_name": {
                    -1: "rotate_left",
                    0: "maintain",
                    1: "rotate_right",
                }[action],
                "reward": round(reward, 4),
            })

            if done:
                break

        return {
            "target_angle": self.target_angle,
            "start_angle": start_angle,
            "start_angular_velocity": start_velocity,
            "steps": len(history),
            "success": done,
            "final_angle": round(self.state.angle, 4),
            "final_angular_velocity": round(self.state.angular_velocity, 4),
            "history": history,
        }
