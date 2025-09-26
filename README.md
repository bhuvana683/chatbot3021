
# Chatbot Platform – Step-by-Step Guide

## 1️) Cloud Demo 

All services are hosted in the cloud, no local setup needed.

* **Backend (FastAPI + Swagger):**
  [https://chatbot3021.onrender.com/docs](https://chatbot3021.onrender.com/docs)
  This is where all API endpoints are documented and testable.

* **Frontend (React + Vite):**
  [https://chatbot3021frontend.onrender.com](https://chatbot3021frontend.onrender.com)
  This is the interactive web interface.

### Cloud Usage Steps

1. Open frontend link in browser.
2. Click **Register** and create a new account.
3. Login with your registered email and password.
4. On the Projects page, either select an existing project or create a new project.
5. Click **Chat** to open the chat interface.
6. Type a message and press **Send**. The chatbot responds using the backend APIs.

---

## 2️) Local Setup 

### Step 1: Clone Repository

```bash
git clone https://github.com/<your-username>/chatbot3021.git
cd chatbot3021
```

### Step 2: Backend Setup

1. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

2. Install backend dependencies:

```bash
pip install -r requirements.txt
```

3. Set environment variables:

```bash
export DATABASE_URL="postgresql://<user>:<password>@localhost:5432/chatbot"
export SECRET_KEY="your_secret_key"
export CHAT_PROJECT_API=//(i used groq( that has more limit))
```

4. Run FastAPI server:

```bash
uvicorn main:app --reload
# Backend runs at http://127.0.0.1:8000
```

5. Optional: Open Swagger docs to test endpoints:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Step 3: Frontend Setup

1. Navigate to frontend folder:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Create `.env` file for API URL:

```bash
echo "VITE_API_URL=http://127.0.0.1:8000" > .env
```

4. Start frontend:

```bash
npm run dev
# Frontend runs at http://localhost:5173
```

---

### Step 4: Testing Locally

1. Open [http://localhost:5173](http://localhost:5173)
2. Register → Login → Create/Select Project → Chat
3. Backend responses come from your local FastAPI server.

---

i check the backend by swagger UI that i sahre in demo  , you can also check by POSTMAN API
if you  want to  just check by frontend ui use  https://chatbot3021frontend.onrender.com
