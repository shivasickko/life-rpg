from pydantic import BaseModel
from typing import Optional, Dict


class RegisterRequest(BaseModel):
username: str


class LoginRequest(BaseModel):
username: str


class Stats(BaseModel):
level: int
xp: int
strength: int
intelligence: int
charisma: int


class StatsUpdate(BaseModel):
level: Optional[int]
xp: Optional[int]
strength: Optional[int]
intelligence: Optional[int]
charisma: Optional[int]


class User(BaseModel):
id: str
username: str
stats: Stats
token: str


class SimulateRequest(BaseModel):
age: int
hours_studied_per_week: float
social_hours_per_week: float
sleep_hours: float