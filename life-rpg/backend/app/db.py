# tiny in-memory DB — replace with real DB (MongoDB/Postgres) later
from typing import Optional


class InMemoryDB:
def __init__(self):
self.users = {}


def create_user(self, user: dict):
self.users[user["id"]] = user


def get_user_by_username(self, username: str) -> Optional[dict]:
for u in self.users.values():
if u.get("username") == username:
return u
return None


def get_user_by_token(self, token: str) -> Optional[dict]:
for u in self.users.values():
if u.get("token") == token:
return u
return None


def get_user_by_id(self, user_id: str) -> Optional[dict]:
return self.users.get(user_id)


def update_user(self, user_id: str, changes: dict):
if user_id not in self.users:
return False
self.users[user_id].update(changes)
return True