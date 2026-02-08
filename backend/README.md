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
- GET /api/v1/health-data/ (requires header X-User-Id)
- POST /api/v1/health-data/ (requires header X-User-Id)

Note: For demo simplicity health-data endpoints accept header `X-User-Id` to identify user. Replace with proper JWT dependency in production.
