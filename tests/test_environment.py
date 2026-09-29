from app.environment import SatelliteEnv

def test_step_changes_state():
    env = SatelliteEnv(target_angle=0)
    env.reset(45, 0)
    state, reward, done = env.step(-1)
    assert state.angle < 45
    assert isinstance(reward, float)
    assert isinstance(done, bool)

def test_invalid_action():
    env = SatelliteEnv()
    try:
        env.step(99)
        assert False
    except ValueError:
        assert True
