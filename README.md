

# Chatbot Platform

## Overview

The Chatbot Platform allows users to create projects, manage prompts, and chat with an AI bot. It has a React frontend with TypeScript and Tailwind CSS, and a FastAPI backend with PostgreSQL and JWT-based authentication.

## Features

* User registration and login with JWT
* Create and manage projects
* Chat with AI bot
* Passwords securely hashed
* Reusable frontend components

## Tech Stack

* **Frontend:** React (Vite), TypeScript, Tailwind CSS
* **Backend:** FastAPI, Python, SQLAlchemy, PostgreSQL
* **Authentication:** JWT
* **API:** REST endpoints
* **Deployment:** Frontend on Vercel/Netlify, Backend on Uvicorn

## Installation

**Backend**

```bash
git clone <repo-url>
cd backend
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

## Usage

1. Register or login.
2. Create or select a project.
3. Send messages in chat.

## Security

* JWT authentication for protected routes
* Passwords hashed with bcrypt
* Authorization header verified on each request



