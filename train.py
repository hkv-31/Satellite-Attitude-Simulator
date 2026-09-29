from app.q_learning import train, save_q_table
from app.config import MODEL_PATH

if __name__ == "__main__":
    print("Training Q-learning agent...")
    q = train(episodes=5000)
    save_q_table(q, MODEL_PATH)
    print(f"Saved Q-table to {MODEL_PATH}")
    print(f"States learned: {len(q)}")
