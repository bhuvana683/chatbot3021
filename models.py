# ---------------------------
# File: models.py
# ---------------------------

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# ---------------------------
# User model
# ---------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)  # Store hashed password
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship: One user can have multiple projects
    projects = relationship("Project", backref="user")


# ---------------------------
# Project model
# ---------------------------
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Link project to user
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship: One project can have multiple prompts
    prompts = relationship("Prompt", backref="project")


# ---------------------------
# Prompt model
# ---------------------------
class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))  # Link prompt to project
    created_at = Column(DateTime, default=datetime.utcnow)
