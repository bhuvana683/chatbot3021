# ---------------------------
# File: main.py
# ---------------------------

# ---------------------------
# Imports
# ---------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import traceback  # For printing detailed error tracebacks
import sys

# ---------------------------
# Try/Except block to catch errors during startup
# ---------------------------
try:
    print("🚀 Initializing FastAPI app...", flush=True)
    # ---------------------------
    # Initialize FastAPI app
    # ---------------------------
    app = FastAPI(title="Chatbot Platform")

    print("🚀 Adding CORS middleware...", flush=True)
    # ---------------------------
    # Enable CORS
    # Allow all origins temporarily for debugging
    # ---------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Change to your frontend URL in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    print("🚀 Importing routers...", flush=True)
    # ---------------------------
    # Import and include routers
    # Wrapping in try/except helps catch import or initialization errors
    # ---------------------------
    from routers import auth, projects, prompts, chat

    print("🚀 Including routers...", flush=True)
    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(projects.router, prefix="/projects", tags=["Projects"])
    app.include_router(prompts.router, prefix="/prompts", tags=["Prompts"])
    app.include_router(chat.router, prefix="/chat", tags=["Chat"])

    print("🚀 Defining root endpoint...", flush=True)
    # ---------------------------
    # Root endpoint to test server
    # ---------------------------
    @app.get("/")
    def root():
        return {"message": "Chatbot Platform API is running"}

except Exception:
    print("🚨 ERROR DURING APP INITIALIZATION 🚨", file=sys.stderr, flush=True)
    traceback.print_exc()
    raise  # Re-raise so Railway logs the error

# ---------------------------
# Run the app (local dev and Railway)
# ---------------------------
if __name__ == "__main__":
    print("🚀 Starting Uvicorn server...", flush=True)
    # Railway sets PORT environment variable; fallback to 8000 locally
    port = int(os.environ.get("PORT", 8000))

    # 0.0.0.0 allows external access (required for Railway)
    uvicorn.run(app, host="0.0.0.0", port=port)
