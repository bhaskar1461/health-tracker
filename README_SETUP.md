Quick Setup (local SQLite - recommended for first run)

1. Backend

```bash
cd health-tracker/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://localhost:8000/docs

2. Frontend
Open `health-tracker/frontend/index.html` in browser (or serve it via `python -m http.server` in that folder).

3. Create/demo user

Use `POST /api/v1/auth/signup` with JSON `{ "email":"test@example.com","password":"test" }` then use header `X-User-Id` with the returned id for health-data endpoints.

Docker (Postgres)

```bash
docker-compose up --build
```

This will start Postgres and backend. Set `DATABASE_URL` if needed.
