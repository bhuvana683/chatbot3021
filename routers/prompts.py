# ---------------------------
# File: routers/prompts.py
# ---------------------------

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Prompt, Project, User
from .auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

# ---------------------------
# Pydantic schema for Prompts
# ---------------------------
class PromptSchema(BaseModel):
    text: str  # The prompt text
    project_id: int  # Link prompt to a project

# ---------------------------
# Create a new prompt (CRUD: Create)
# ---------------------------
@router.post("/")
def create_prompt(
    data: PromptSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prompt = Prompt(
        text=data.text,
        project_id=data.project_id
    )
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    return prompt

# ---------------------------
# List all prompts (CRUD: Read)
# ---------------------------
@router.get("/")
def list_prompts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Fetch only prompts whose project belongs to the current user
    prompts = db.query(Prompt).join(Project).filter(Project.user_id == current_user.id).all()
    return prompts

# ---------------------------
# Get a single prompt (CRUD: Read)
# ---------------------------
@router.get("/{prompt_id}")
def get_prompt(
    prompt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

# ---------------------------
# Update a prompt (CRUD: Update)
# ---------------------------
@router.put("/{prompt_id}")
def update_prompt(
    prompt_id: int,
    data: PromptSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    prompt.text = data.text
    prompt.project_id = data.project_id
    db.commit()
    db.refresh(prompt)
    return prompt

# ---------------------------
# Delete a prompt (CRUD: Delete)
# ---------------------------
@router.delete("/{prompt_id}")
def delete_prompt(
    prompt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    db.delete(prompt)
    db.commit()
    return {"message": "Prompt deleted successfully"}
