# Backend (FastAPI)

Run locally with SQLite (default):

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API endpoints:
- POST /api/v1/auth/signup {email,password}
- POST /api/v1/auth/login {email,password}
- GET /api/v1/health-data/ (requires Authorization: Bearer <token>)
- POST /api/v1/health-data/ (requires Authorization: Bearer <token>)

Note: Health-data endpoints require JWT access tokens from /auth/login.
