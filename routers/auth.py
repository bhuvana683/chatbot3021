# routers/auth.py

import os
from fastapi import APIRouter, Depends, HTTPException  # FastAPI classes for routing, dependency injection, and errors
from pydantic import BaseModel, EmailStr               # Pydantic for request data validation
from sqlalchemy.orm import Session                     # SQLAlchemy session type
from passlib.hash import bcrypt                        # For hashing passwords securely
from jose import jwt                                   # For creating and decoding JWT tokens
from database import get_db                            # Function to get a DB session
from models import User                                # User model from SQLAlchemy
from dotenv import load_dotenv                         # Load environment variables from .env file
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  # For token-based auth

# Load environment variables from .env
load_dotenv()

# Get the secret key for JWT from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")

# Create a FastAPI router for auth-related routes
router = APIRouter()

# -----------------------------
# Pydantic Schemas for validation
# -----------------------------
class RegisterSchema(BaseModel):
    name: str                  # Full name of user
    email: EmailStr            # Email (validated automatically)
    password: str              # Password (will be hashed before storing)

class LoginSchema(BaseModel):
    email: EmailStr            # Email for login
    password: str              # Password for login

# -----------------------------
# Authentication Helper
# -----------------------------

# Use HTTP Bearer scheme for token-based authentication
bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),  # Automatically get token from request
    db: Session = Depends(get_db)                                       # DB session dependency
):
    """
    Decode JWT token and return the current logged-in user.
    Raises 401 if token is invalid or user does not exist.
    """
    token = credentials.credentials  # Extract token string from header
    try:
        # Decode token using SECRET_KEY and HS256 algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Query user from database
        user = db.query(User).filter(User.id == payload["user_id"]).first()
        if not user:
            # If user not found, raise HTTP 401
            raise HTTPException(status_code=401, detail="Invalid authentication")
        return user  # Return the user object
    except Exception as e:
        print("Token decode error:", e)  # Debugging print
        raise HTTPException(status_code=401, detail="Invalid token")

# -----------------------------
# User Registration Endpoint
# -----------------------------
@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    """
    Register a new user.
    Checks if email exists, hashes password, saves user in database.
    Returns user ID on success.
    """
    # Check if email already exists in DB
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Create new User object and hash password
    user = User(
        name=data.name,
        email=data.email,
        password_hash=bcrypt.hash(data.password)  # Hash the password
    )

    # Add to DB and commit transaction
    db.add(user)
    db.commit()
    db.refresh(user)  # Refresh user to get ID from DB

    # Return success response with user ID
    return {"message": "User registered successfully", "user_id": user.id}

# -----------------------------
# User Login Endpoint
# -----------------------------
@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    """
    Login a user.
    Verifies email and password, returns JWT token if valid.
    """
    # Fetch user from DB by email
    user = db.query(User).filter(User.email == data.email).first()

    # Check if user exists and password is correct
    if not user or not bcrypt.verify(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Encode JWT token with user ID
    token = jwt.encode({"user_id": user.id}, SECRET_KEY, algorithm="HS256")

    # Return token to client
    return {"access_token": token}
