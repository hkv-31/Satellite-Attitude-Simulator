import os

FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "simulations")
MODEL_PATH = os.getenv("MODEL_PATH", "model/q_table.json")

ANGLE_MIN = -180
ANGLE_MAX = 180
ANGLE_STEP = 5

VELOCITY_MIN = -10
VELOCITY_MAX = 10
VELOCITY_STEP = 1

ACTIONS = (-1, 0, 1)  # left, maintain, right
ACTION_NAMES = {-1: "rotate_left", 0: "maintain", 1: "rotate_right"}

TARGET_DEFAULT = 0
MAX_STEPS_DEFAULT = 100
