from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .config import MODEL_PATH, MAX_STEPS_DEFAULT
from .environment import SatelliteEnv
from .q_learning import load_q_table
from .storage import save_simulation
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Satellite Attitude Control Simulator",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "https://satellite-attitude-sim.web.app", 
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

Q_TABLE = load_q_table(MODEL_PATH)

class SimulationRequest(BaseModel):
    target_angle: float = Field(0, ge=-180, le=180)
    start_angle: float = Field(45, ge=-180, le=180)
    start_angular_velocity: float = Field(0, ge=-10, le=10)
    max_steps: int = Field(MAX_STEPS_DEFAULT, ge=1, le=200)

@app.get("/")
def root():
    return {
        "name": "Satellite Attitude Control Simulator",
        "status": "ok",
        "docs": "/docs",
    }

@app.get("/health")
def health():
    return {"status": "healthy", "q_table_states": len(Q_TABLE)}

@app.post("/simulate")
def simulate(request: SimulationRequest):
    try:
        env = SatelliteEnv(target_angle=request.target_angle)
        result = env.simulate(
            Q_TABLE,
            start_angle=request.start_angle,
            start_velocity=request.start_angular_velocity,
            max_steps=request.max_steps,
        )
        doc_id = save_simulation(result)
        result["storage_status"] = "saved" if doc_id else "disabled"
        result["simulation_id"] = doc_id
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
