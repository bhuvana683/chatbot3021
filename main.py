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

# ---------------------------
# Try/Except block to catch errors during startup
# ---------------------------
try:
    # ---------------------------
    # Initialize FastAPI app
    # ---------------------------
    app = FastAPI(title="Chatbot Platform")

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

    # ---------------------------
    # Import and include routers
    # Wrapping in try/except helps catch import or initialization errors
    # ---------------------------
    from routers import auth, projects, prompts, chat

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

# ---------------------------
# Catch any errors during startup and print them
# ---------------------------
except Exception:
    print("🚨 ERROR DURING APP INITIALIZATION 🚨")
    traceback.print_exc()  # Prints full Python error
    raise  # Re-raise so Railway logs the error

# ---------------------------
# Run the app (local dev and Railway)
# ---------------------------
if __name__ == "__main__":
    # Railway sets PORT environment variable; fallback to 8000 locally
    port = int(os.environ.get("PORT", 8000))

    # 0.0.0.0 allows external access (required for Railway)
    uvicorn.run(app, host="0.0.0.0", port=port)
