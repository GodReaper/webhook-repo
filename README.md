# GitHub Webhook Application

A monorepo application that receives GitHub webhooks and displays real-time repository activity.

## Features

- Receives GitHub webhook events (push, pull request, merge)
- Real-time event feed with 15-second polling
- MongoDB storage for event persistence
- React frontend with Tailwind CSS
- Flask backend API

## Docker Setup

### Prerequisites

- Docker
- Docker Compose

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gh-webhook
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5001
   - MongoDB: localhost:27017

### Services

- **Frontend**: React application served by Nginx (port 3000)
- **Backend**: Flask API server (port 5001)
- **MongoDB**: Database for storing webhook events (port 27017)

### Environment Variables

The application uses the following environment variables:

- `MONGODB_URI`: MongoDB connection string (default: mongodb://admin:password@mongodb:27017/webhook_db?authSource=admin)
- `MONGODB_DB`: Database name (default: webhook_db)
- `FLASK_ENV`: Flask environment (default: production)

### Development

For local development without Docker:

1. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python run.py
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **MongoDB Setup**
   - Install MongoDB locally or use Docker: `docker run -d -p 27017:27017 --name mongodb mongo:7.0`

## API Endpoints

- `GET /api/events` - Get events from the last 15 seconds
- `POST /webhook/github` - GitHub webhook endpoint

## Webhook Configuration

Configure your GitHub repository webhook to point to:
- URL: `http://your-domain/webhook/github`
- Content type: `application/json`
- Events: Push, Pull request

## Docker Commands

```bash
# Build and start all services
docker-compose up --build

# Start services in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes (clears database)
docker-compose down -v

# Rebuild specific service
docker-compose build backend

# Access container shell
docker-compose exec backend bash
docker-compose exec frontend sh
docker-compose exec mongodb mongosh
```

# GitHub Webhook Activity Feed Monorepo

A full-stack project to capture GitHub repository events (Push, Pull Request, Merge) via webhooks, store them in MongoDB, and display them in a live-updating, minimal UI.

---

## Features
- **Webhook Receiver:** Flask backend receives GitHub webhooks, authenticates them, and stores normalized events in MongoDB Atlas.
- **Live UI:** React + Vite + Tailwind frontend polls the backend every 15 seconds and displays the latest repo activity in a clean, minimal feed.
- **Secure:** Webhook endpoint requires a secret header for authentication.
- **Merge Detection:** Merges are inferred from pull request events.

---

## Architecture

```
GitHub Repo (action-repo)
   │
   └──> [ngrok tunnel] ──> Flask Webhook Receiver (backend/) ──> MongoDB Atlas
                                              │
                                              └──> React UI (frontend/) polls /api/events
```

---

## Tech Stack
- **Backend:** Python, Flask, Flask-CORS, PyMongo, python-dotenv
- **Frontend:** React, Vite, Tailwind CSS
- **Database:** MongoDB Atlas (cloud)
- **Dev Tools:** ngrok (for public webhook endpoint), venv, npm

---

## Setup Instructions

### 1. Clone the Repo
```sh
git clone <your-repo-url>
cd <repo-root>
```

### 2. Backend Setup (Flask)
```sh
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Fill in your MongoDB Atlas URI and webhook secret
```

#### Environment Variables (`backend/.env`)
- `MONGODB_URI` - Your MongoDB Atlas connection string
- `WEBHOOK_SECRET` - Secret token for authenticating incoming webhooks

### 3. Frontend Setup (React + Vite + Tailwind)
```sh
cd ../frontend
npm install
```

#### (Optional) Set API Base URL
If your backend is running on ngrok, create a `.env` file in `frontend/`:
```
VITE_API_BASE_URL=https://<your-ngrok-subdomain>.ngrok-free.app
```
And update your fetch calls to use this variable.

### 4. Running Locally
- **Start Backend:**
  ```sh
  cd backend
  source venv/bin/activate
  python -m app.main
  # or
  export FLASK_APP=app.main
  flask run --host=0.0.0.0 --port=5000
  ```
- **Expose Backend (for GitHub webhooks):**
  ```sh
  ngrok http 5000
  # Use the https URL for your GitHub webhook config
  ```
- **Start Frontend:**
  ```sh
  cd frontend
  npm run dev
  # Open the local address shown in your terminal
  ```

---

## Usage
1. **Configure GitHub Webhook:**
   - Set the webhook URL to your ngrok HTTPS URL + `/webhook` (e.g., `https://xxxx.ngrok-free.app/webhook`).
   - Set the webhook secret to match `WEBHOOK_SECRET` in your backend `.env`.
   - Subscribe to Push and Pull Request events.
2. **Trigger Events:**
   - Push, open PRs, and merge PRs in your GitHub repo.
3. **View Activity Feed:**
   - Open the frontend app. The feed will update every 15 seconds with new events.

---

## Example Event Formats
- **Push:** `Travis pushed to staging on 1 April 2021 - 9:30 PM UTC`
- **Pull Request:** `Travis submitted a pull request from staging to master on 1 April 2021 - 9:00 AM UTC`
- **Merge:** `Travis merged branch dev to master on 2 April 2021 - 12:00 PM UTC`

---

## Troubleshooting
- **CORS errors?** Ensure Flask-CORS is installed and enabled in the backend.
- **Ngrok warning page?** Only visit the ngrok URL via your frontend/API, not directly in the browser.
- **No events?** Check your webhook delivery status in GitHub repo settings and your backend logs.

---

## License
MIT 

##Tasks Given by Interviewer
Dockerise the application
add logging to backend 
make it fetch only 15sec event else none (Done)
read celery and msg queues how it works
https://www.tornadoweb.org/en/stable/guide/queues.html read and go through the code 