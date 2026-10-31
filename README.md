# 🏆 Quiz Arena

## 🌐 Live Demo
**Try it here:** https://quiz-arena-omega-navy.vercel.app
## Screenshots
| Login | Home |
|---|---|
| ![Login](screenshots/login.png) | ![Home](screenshots/home.png) |

| Quiz | Result |
|---|---|
| ![Quiz](screenshots/quiz.png) | ![Result](screenshots/result.png) |

| Leaderboard | My History |
|---|---|
| ![Leaderboard](screenshots/leaderboard.png) | ![History](screenshots/history.png) |

> The backend runs on a free plan, so the first load may take up to a minute while it wakes up.

A full stack online quiz platform. Users register, log in, take timed multiple-choice quizzes by category, see their score with an answer review, and compete on a global leaderboard.

**Stack:** Django + Django REST Framework (backend API) · React + Vite (frontend) · SQLite (database) · JWT authentication

## Features
- Register and login with JWT tokens (password validation included)
- 4 sample categories, 40 questions (Python, SQL, AI & ML, General Knowledge)
- 10 random questions per quiz with a 15-second timer per question
- Scoring is done **on the server**, and correct answers are never sent to the browser
- Result page with a full answer review
- Leaderboard (top 10 players) and personal attempt history
- Django admin panel to manage categories and questions
- 9 automated backend tests

## Project structure
```
quiz-arena/
├── backend/            Django project
│   ├── config/         settings and main urls
│   ├── quiz/           models, serializers, views, urls, tests, seed command
│   ├── manage.py
│   └── requirements.txt
└── frontend/           React app (Vite)
    └── src/
        ├── api.js      axios setup + JWT token handling
        ├── App.jsx     routes
        ├── components/ Navbar
        └── pages/      Login, Register, Home, Quiz, Result, Leaderboard, History
```

## API endpoints
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| POST | /api/register/ | No | Create account |
| POST | /api/login/ | No | Get JWT access token |
| GET | /api/categories/ | No | List categories |
| GET | /api/questions/?category=1&limit=10 | No | Random questions (no answers) |
| POST | /api/submit/ | Yes | Score answers and save attempt |
| GET | /api/leaderboard/ | No | Top 10 players |
| GET | /api/history/ | Yes | Logged-in user's attempts |

## Run it locally

You need Python 3.10+ and Node.js 18+.

### 1. Backend (Terminal 1)
```bash
cd backend
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # Mac / Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py seed            # loads 40 sample questions
python manage.py createsuperuser # for the admin panel (optional)
python manage.py runserver
```
Backend runs at http://127.0.0.1:8000 (admin panel: /admin).

### 2. Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173

### 3. Run the tests
```bash
cd backend
python manage.py test
```

## Deployment (optional)
- **Backend on Render:** add `gunicorn`, `whitenoise` and `psycopg2-binary` to requirements, set `DEBUG=False`, a new `SECRET_KEY`, `ALLOWED_HOSTS` and your frontend URL in `CORS_ALLOWED_ORIGINS`. Start command: `gunicorn config.wsgi`.
- **Frontend on Vercel/Netlify:** set the environment variable `VITE_API_URL` to your backend URL ending with `/api/`. Build command `npm run build`, output folder `dist`.

## Future scope
Real-time multiplayer, AI-generated questions, streaks and badges, analytics dashboard, CSV bulk upload of questions.

## Author
Tejasri · B.Tech AI & Data Science · MVR College of Engineering and Technology
