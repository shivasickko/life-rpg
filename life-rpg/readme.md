Life RPG — Reconstructed


Quick start (backend):
1. cd backend
2. python -m venv .venv
3. source .venv/bin/activate # on Windows: .venv\Scripts\activate
4. pip install -r requirements.txt
5. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


Quick start (frontend):
1. cd web
2. npm install
3. npm start


Notes:
- Replace the placeholder `models/life_model.joblib` with a real joblib model if you have one.
- For production, swap the in-memory DB for MongoDB/Postgres and add proper auth (JWT/password hashing).