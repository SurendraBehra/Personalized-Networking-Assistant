# Production Deployment Guide - NetConnect

This document details strategies and steps to deploy the **NetConnect (Personalized Networking Assistant)** application to production environments.

---

## 1. Production Architecture Considerations

For production environments, we recommend making the following adjustments to scale and secure the application:

- **Database**: Swap the local SQLite database for a managed database engine like **PostgreSQL** or **MySQL**.
  - Update `DATABASE_URL` in your `.env` (SQLAlchemy supports `postgresql://user:password@host/db`).
- **CORS Configuration**: Restrict the `allow_origins` settings in `backend/app/main.py` from `["*"]` to your specific frontend URL domain.
- **SSL Certificates**: Always serve APIs and Web Frontends over HTTPS (using Nginx, Cloudflare, or Load Balancers).

---

## 2. Dockerized Deployment (Recommended)

You can containerize the backend and frontend separately to host them on AWS, GCP, Azure, Render, or Railway.

### Backend `Dockerfile`
Create a `backend.Dockerfile` in `05_Project_Development/`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend `Dockerfile`
Create a `frontend.Dockerfile` in `05_Project_Development/`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY frontend/ ./frontend/

EXPOSE 8501

CMD ["streamlit", "run", "frontend/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

---

## 3. Deployment Options

### Option A: Streamlit Community Cloud (Frontend Only)
You can deploy your frontend directly to [Streamlit Community Cloud](https://streamlit.io/cloud):
1. Push your code repository to GitHub.
2. Link your GitHub account to Streamlit Community Cloud.
3. Configure the main entrypoint file path as `05_Project_Development/frontend/app.py`.
4. Define your backend production API URL in Streamlit's secrets manager as `BACKEND_URL`.

### Option B: Render, Railway, or Heroku
You can deploy both parts of the application easily using PaaS providers like **Render** or **Railway**:

1. **Deploy Backend**:
   - Create a Web Service linked to your Git repository.
   - Set Build Command: `pip install -r 05_Project_Development/requirements.txt`
   - Set Start Command: `uvicorn 05_Project_Development.backend.app.main:app --host 0.0.0.0 --port $PORT`
   - Configure Environment Variables:
     - `DATABASE_URL`: Your production database URL.
     - `GEMINI_API_KEY`: Your production Gemini API Key.
   - Copy the public URL of the deployed backend (e.g. `https://netconnect-api.onrender.com`).

2. **Deploy Frontend**:
   - Create another Web Service linked to the same Git repository.
   - Set Build Command: `pip install -r 05_Project_Development/requirements.txt`
   - Set Start Command: `streamlit run 05_Project_Development/frontend/app.py --server.port $PORT`
   - Configure Environment Variables:
     - `BACKEND_URL`: Paste the public URL of the backend service created in step 1.
