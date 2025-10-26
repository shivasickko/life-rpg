from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict
from fastapi.middleware.cors import CORSMiddleware
from app.models.predictor import LifeModel
from app.db import InMemoryDB
import uuid

app = FastAPI(title="Life RPG Backend")


# Allow CORS from frontend during local development
app.add_middleware(
CORSMiddleware,
allow_origins=["http://localhost:3000"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

# simple in-memory DB (replace with MongoDB / PostgreSQL later)
db = InMemoryDB()
model = LifeModel.load("../../models/life_model.joblib") 
# path relative to main.py when running from /backend


class RegisterRequest(BaseModel):
username: str


class LoginRequest(BaseModel):
username: str


class StatsUpdate(BaseModel):
level: Optional[int]
xp: Optional[int]
strength: Optional[int]
intelligence: Optional[int]
charisma: Optional[int]

class SimulateRequest(BaseModel):
age: int
hours_studied_per_week: float
social_hours_per_week: float
sleep_hours: float


@app.get("/health")
def health():
return {"status": "ok"}


@app.post("/register")
def register(req: RegisterRequest):
if db.get_user_by_username(req.username):
raise HTTPException(status_code=400, detail="username already exists")
user_id = str(uuid.uuid4())
user = {
"id": user_id,
"username": req.username,
"stats": {"level": 1, "xp": 0, "strength": 5, "intelligence": 5, "charisma": 5},
"token": str(uuid.uuid4())
}
db.create_user(user)
return {"user": user}

@app.post("/login")
def login(req: LoginRequest):
user = db.get_user_by_username(req.username)
if not user:
raise HTTPException(status_code=404, detail="user not found")
return {"token": user["token"], "user": user}


# dependency to fetch user by token
def get_current_user(token: str = ""):
user = db.get_user_by_token(token)
if not user:
raise HTTPException(status_code=401, detail="invalid token")
return user


@app.get("/user/me")
def me(token: Optional[str] = ""):
return get_current_user(token)


@app.get("/user/{user_id}/stats")
def get_stats(user_id: str):
user = db.get_user_by_id(user_id)
if not user:
raise HTTPException(404, "user not found")
return user["stats"]

@app.put("/user/{user_id}/stats")
def update_stats(user_id: str, update: StatsUpdate):
user = db.get_user_by_id(user_id)
if not user:
raise HTTPException(404, "user not found")
stats = user.get("stats", {})
for field in ["level", "xp", "strength", "intelligence", "charisma"]:
if getattr(update, field, None) is not None:
stats[field] = getattr(update, field)
db.update_user(user_id, {"stats": stats})
return {"stats": stats}


@app.get("/quests")
def get_quests():
# simple static quests; replace with dynamic generation logic later
quests = [
{"id": "q1", "title": "Finish a mini project", "xp": 50},
{"id": "q2", "title": "Read a technical article", "xp": 20},
{"id": "q3", "title": "Go for a run", "xp": 15}
]
return {"quests": quests}


@app.post("/simulate")
def simulate(req: SimulateRequest):
# example: model.predict_proba or model.predict
features = [req.age, req.hours_studied_per_week, req.social_hours_per_week, req.sleep_hours]
try:
result = model.predict_single(features)
except Exception as e:
raise HTTPException(500, f"model error: {e}")
return {"simulation": result}