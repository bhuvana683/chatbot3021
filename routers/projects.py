# ---------------------------
# File: routers/projects.py
# ---------------------------

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models import Project, User
from .auth import get_current_user
from pydantic import BaseModel
import os, shutil

router = APIRouter()

# ---------------------------
# Pydantic schema for Projects
# ---------------------------
class ProjectSchema(BaseModel):
    name: str  # Project name
    description: str | None = None  # Optional project description

# ---------------------------
# Create a new project (CRUD: Create)
# ---------------------------
@router.post("/")
def create_project(
    data: ProjectSchema,  # Data from request body
    current_user: User = Depends(get_current_user),  # Get current logged-in user
    db: Session = Depends(get_db)  # Database session
):
    project = Project(
        name=data.name,  # Assign project name
        description=data.description,  # Assign description
        user_id=current_user.id  # Link to logged-in user
    )
    db.add(project)  # Add project to session
    db.commit()  # Commit to database
    db.refresh(project)  # Refresh object
    return project  # Return newly created project

# ---------------------------
# List all projects (CRUD: Read)
# ---------------------------
@router.get("/")
def list_projects(
    current_user: User = Depends(get_current_user),  # Only show user's projects
    db: Session = Depends(get_db)
):
    projects = db.query(Project).filter(Project.user_id == current_user.id).all()
    return projects

# ---------------------------
# Get a single project by ID (CRUD: Read)
# ---------------------------
@router.get("/{project_id}")
def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# ---------------------------
# Update a project (CRUD: Update)
# ---------------------------
@router.put("/{project_id}")
def update_project(
    project_id: int,
    data: ProjectSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Update project fields
    project.name = data.name
    project.description = data.description
    db.commit()
    db.refresh(project)
    return project

# ---------------------------
# Delete a project (CRUD: Delete)
# ---------------------------
@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}

# ---------------------------
# Upload a file to a project
# ---------------------------
@router.post("/{project_id}/upload")
def upload_file(
    project_id: int,
    file: UploadFile = File(...),  # Receive file from request
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify project belongs to user
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Ensure upload folder exists
    os.makedirs("uploads", exist_ok=True)

    # Save file to local uploads folder
    file_path = f"uploads/{project_id}_{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Return success message
    return {"message": "File uploaded successfully", "file_path": file_path}
