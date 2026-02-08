# Health Tracker with Zepp Integration

A full-stack health tracking application that syncs data directly from Zepp (Xiaomi/Amazfit) devices.

## 🚀 Features

- **FastAPI Backend** with SQLAlchemy ORM
- **JWT Authentication** for secure user management
- **Health Data Tracking** with comprehensive metrics
- **Zepp App Integration** - Sync fitness data directly from Xiaomi/Amazfit devices
- **Modern Frontend** with interactive charts and activity rings
- **Docker Support** for easy deployment
- **SQLite/PostgreSQL** database support

## 📊 Health Metrics Tracked

- Calories burned
- Exercise minutes
- Stand hours
- Resting heart rate
- Respiratory rate
- Sleep duration and quality
- Sleep stages (REM, Core, Deep)

## 🏗️ Architecture

```
health-tracker/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/v1/         # API endpoints
│   │   ├── core/           # Configuration
│   │   ├── crud/           # Database operations
│   │   ├── db/             # Database setup
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # External services (Zepp)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                # Static HTML/CSS/JS
│   ├── index.html
│   ├── app.js
│   └── styles.css
└── docker-compose.yml
```

## 🛠️ Quick Start

### Local Development (SQLite)

1. **Clone and setup backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Zepp credentials (optional):**
   ```bash
   cp .env.example .env
   # Edit .env and add:
   # ZEPP_PHONE=your_zepp_phone_number
   # ZEPP_PASSWORD=your_zepp_password
   ```

3. **Start the backend:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Start the frontend:**
   ```bash
   cd ../frontend
   python -m http.server 3000
   ```

5. **Open your browser:**
   - **API Documentation**: http://localhost:8000/docs
   - **Web App**: http://localhost:3000

### Docker (PostgreSQL)

```bash
docker-compose up --build
```

## 🔄 Zepp Integration

### Setup

1. **Get your Zepp credentials:**
   - Phone number and password used for Zepp app login

2. **Configure environment:**
   ```bash
   cd backend
   # Add to .env file:
   ZEPP_PHONE=your_phone_number
   ZEPP_PASSWORD=your_password
   ```

3. **Sync data:**
   - Open the web app
   - Click "Sync from Zepp" button
   - Your latest fitness data will be imported

### What Gets Synced

- **Steps & Calories**: Primary activity metrics
- **Heart Rate**: Resting heart rate data
- **Sleep Data**: Duration, quality, and stages
- **Exercise**: Activity minutes and stand hours

### API Endpoint

```bash
POST /api/v1/health-data/sync-zepp
Headers: X-User-Id: <user_id>
```

## 📱 API Usage

### Authentication

The app uses a simple demo authentication with `X-User-Id` header. In production, implement proper JWT authentication.

### Create User

```bash
POST http://localhost:8000/api/v1/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### Add Health Data

```bash
POST http://localhost:8000/api/v1/health-data/
Content-Type: application/json
X-User-Id: 1

{
  "calories_burned": 450,
  "exercise_minutes": 30,
  "stand_hours": 8,
  "resting_heart_rate": 65,
  "sleep_duration": 8.5,
  "sleep_quality": 4
}
```

### Sync from Zepp

```bash
POST http://localhost:8000/api/v1/health-data/sync-zepp
X-User-Id: 1
```

## 🗄️ Database

### Models

- **User**: Authentication and profile
- **HealthData**: Daily health metrics with timestamp

### Migrations

```bash
cd backend
alembic revision --autogenerate -m "Add new table"
alembic upgrade head
```

## 🔧 Development

### Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

### Frontend Development

The frontend is pure HTML/CSS/JS - no build process required. Just edit the files in `frontend/` directory.

### Testing

```bash
cd backend
pytest
```

## 🚀 Deployment

### Docker Compose

```bash
docker-compose up -d
```

### Environment Variables

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/health_tracker
ZEPP_PHONE=your_phone
ZEPP_PASSWORD=your_password
SECRET_KEY=your-secret-key
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Disclaimer

- This project is for educational purposes
- Zepp integration requires valid Zepp app credentials
- Data syncing may be subject to Zepp's terms of service
- Always backup your health data

## 🆘 Troubleshooting

### Common Issues

1. **"Zepp credentials not configured"**
   - Add `ZEPP_PHONE` and `ZEPP_PASSWORD` to `.env` file

2. **CORS errors**
   - Frontend and backend must be on different ports
   - API calls use absolute URLs to backend

3. **Database connection**
   - Check `DATABASE_URL` in environment
   - For SQLite, use `sqlite:///./dev.db`

### Support

- Check the API documentation at `/docs`
- Review the test page at `frontend/test.html`
- Check server logs for error details

---

**Built with ❤️ using FastAPI, SQLAlchemy, and modern web technologies**
