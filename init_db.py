# init_db.py
from database import engine, Base
from models import User, Medicine, Reminder

print("Initializing the database...")
Base.metadata.create_all(bind=engine)
print("Database initialized successfully.")