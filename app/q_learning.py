import json
import random
from pathlib import Path
from .environment import SatelliteEnv
from .config import ACTIONS

def train(
    episodes=5000,
    alpha=0.15,
    gamma=0.95,
    epsilon=1.0,
    epsilon_min=0.05,
    epsilon_decay=0.995,
    seed=42,
):
    random.seed(seed)
    env = SatelliteEnv(target_angle=0)
    q = {}

    for _ in range(episodes):
        start_angle = random.uniform(-150, 150)
        start_velocity = random.uniform(-5, 5)
        env.reset(start_angle, start_velocity)

        for _ in range(100):
            state = str(env.state_key())
            q.setdefault(state, {str(a): 0.0 for a in ACTIONS})

            if random.random() < epsilon:
                action = random.choice(ACTIONS)
            else:
                action = max(ACTIONS, key=lambda a: q[state][str(a)])

            _, reward, done = env.step(action)
            next_state = str(env.state_key())
            q.setdefault(next_state, {str(a): 0.0 for a in ACTIONS})

            old = q[state][str(action)]
            best_next = max(q[next_state].values())

            q[state][str(action)] = old + alpha * (
                reward + gamma * best_next - old
            )

            if done:
                break

        epsilon = max(epsilon_min, epsilon * epsilon_decay)

    return q

def save_q_table(q_table, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(q_table, indent=2), encoding="utf-8")

def load_q_table(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
