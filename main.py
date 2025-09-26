# ---------------------------
# File: main.py
# ---------------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Added for CORS support
from routers import auth, projects, prompts, chat

# ---------------------------
# Initialize FastAPI app
# ---------------------------
app = FastAPI(title="Chatbot Platform")

# ---------------------------
# Enable CORS for frontend
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Include routers for API endpoints
# ---------------------------
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(prompts.router, prefix="/prompts", tags=["Prompts"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])

# ---------------------------
# Root endpoint to test server
# ---------------------------
@app.get("/")
def root():
    return {"message": "Chatbot Platform API is running"}
