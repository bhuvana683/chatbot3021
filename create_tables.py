# ---------------------------
# File: create_tables.py
# ---------------------------

# Import database Base and engine
from database import Base, engine
import models  # Ensure all models (User, Project, Prompt) are imported

# ---------------------------
# Create tables in the database
# ---------------------------
# This will create all tables based on the models defined in models.py
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
