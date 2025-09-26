# ---------------------------
# File: routers/chat.py
# ---------------------------

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import Project, User
from .auth import get_current_user
import os, requests, shutil
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

router = APIRouter()

# ---------------------------
# Pydantic schema for Chat messages
# ---------------------------
class ChatSchema(BaseModel):
    project_id: int  # ID of the project associated with the chat
    message: str     # User's chat message

# ---------------------------
# Chat with Project (POST)
# ---------------------------
@router.post("/")
def chat_with_project(
    data: ChatSchema,
    current_user: User = Depends(get_current_user),  # Get logged-in user
    db: Session = Depends(get_db)  # Database session
):
    # Verify project ownership before sending chat
    project = db.query(Project).filter(
        Project.id == data.project_id,
        Project.user_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Call external Groq API to generate response
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('CHAT_PROJECT_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",  # Model used for response
                "messages": [{"role": "user", "content": data.message}],
                "max_tokens": 100
            }
        )

        # Check API response status
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Groq API error: {response.text}")

        # Extract reply from API response
        reply = response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq API exception: {e}")

    return {"response": reply}

# ---------------------------
# Upload a file related to chat (Optional)
# ---------------------------
@router.post("/{project_id}/upload")
def upload_chat_file(
    project_id: int,
    file: UploadFile = File(...),  # File uploaded from request
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify project ownership
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Ensure uploads folder exists
    os.makedirs("uploads/chat_files", exist_ok=True)

    # Save file to local directory
    file_path = f"uploads/chat_files/{project_id}_{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {"message": "Chat file uploaded successfully", "file_path": file_path}

# ---------------------------
# Get all chat files for a project
# ---------------------------
@router.get("/{project_id}/files")
def get_chat_files(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify project ownership
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # List all files in uploads/chat_files matching this project
    folder_path = "uploads/chat_files"
    files = [f for f in os.listdir(folder_path) if f.startswith(f"{project_id}_")]
    return {"files": files}

# ---------------------------
# Delete a chat file
# ---------------------------
@router.delete("/{project_id}/files/{filename}")
def delete_chat_file(
    project_id: int,
    filename: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify project ownership
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Delete file from local directory
    file_path = f"uploads/chat_files/{filename}"
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": "Chat file deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="File not found")
