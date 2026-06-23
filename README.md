# Sai Creator — Full-Stack Agency Website

A production-grade **FastAPI** web application for the Sai Creator digital agency.

---

## 🚀 Quick Start (Local Dev)

```bash
# 1. Clone / open the project
cd "teja Agency"

# 2. Create a virtual environment
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env
# (Edit .env with your settings if needed)

# 5. Start the dev server
uvicorn app.main:app --reload --port 8000
```

Open **http://localhost:8000** in your browser.

---

## 🐳 Docker (One Command)

```bash
# Dev: SQLite
docker build -t teja-labs .
docker run -p 8000:8000 --env-file .env teja-labs

# Production: with PostgreSQL
docker-compose up --build
```

---

## 🔐 Admin Dashboard

Visit: **http://localhost:8000/admin**

Default password: `admin123`

> ⚠️ **Change `ADMIN_PASSWORD` in `.env` before deploying to production!**

---

## 📡 API Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Landing page |
| `GET` | `/admin` | Admin login |
| `POST` | `/admin` | Admin login form |
| `POST` | `/api/contact` | Submit contact form |
| `GET` | `/api/leads?token=<pw>` | List all leads (JSON) |
| `DELETE` | `/api/leads/{id}?token=<pw>` | Delete a lead |
| `GET` | `/api/health` | Health check |
| `GET` | `/api/docs` | Interactive API docs (dev only) |

---

## ☁️ Deploy to Railway

1. Push repo to **GitHub**
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**
3. Add a **PostgreSQL** service (click + Add)
4. Set environment variables:
   - `DATABASE_URL` → auto-set by Railway when you link the Postgres service
   - `APP_ENV` → `production`
   - `ADMIN_PASSWORD` → your secure password
   - `ALLOWED_ORIGINS` → your domain (e.g., `https://tejlabs.com`)
   - `SECRET_KEY` → random 64-char string
5. Deploy! 🚀

---

## ☁️ Deploy to Render

1. Push repo to **GitHub**
2. Go to [render.com](https://render.com) → **New** → **Blueprint**
3. Connect your repo — Render reads `render.yaml` automatically
4. Set `ADMIN_PASSWORD` manually in the Render dashboard
5. Deploy!

---

## 📧 Email Notifications (Optional)

To receive email alerts when someone submits the contact form, set these in `.env`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=you@gmail.com
SMTP_PASSWORD=your-gmail-app-password  # NOT your regular password
NOTIFICATION_EMAIL=you@yourcompany.com
```

Gmail tip: Enable 2FA → create an **App Password** at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).

---

## 🗄️ Database

- **Development**: SQLite (`teja_agency.db` in project root) — zero config
- **Production**: Set `DATABASE_URL=postgresql://user:pass@host:5432/dbname`

Tables are auto-created on startup.

---

## 📁 Project Structure

```
teja Agency/
├── app/
│   ├── main.py         # FastAPI app + middleware
│   ├── config.py       # Settings from .env
│   ├── database.py     # SQLAlchemy engine
│   ├── models.py       # DB models
│   ├── schemas.py      # Pydantic schemas
│   ├── email_utils.py  # Email notifications
│   └── routers/
│       ├── pages.py    # HTML page routes
│       └── api.py      # REST API routes
├── templates/
│   ├── index.html      # Landing page
│   ├── admin_login.html
│   └── admin.html      # Admin dashboard
├── static/
│   ├── css/main.css
│   └── js/main.js
├── .env                # Local secrets (git-ignored)
├── .env.example        # Template for secrets
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── gunicorn.conf.py    # Production server config
├── railway.toml        # Railway deploy config
└── render.yaml         # Render deploy config
```

---

## 🛡️ Security Notes

- Change `ADMIN_PASSWORD` and `SECRET_KEY` before going live
- Set `ALLOWED_ORIGINS` to your actual domain in production
- API docs (`/api/docs`) are disabled in production (`APP_ENV=production`)
- The app runs as a non-root user in Docker
