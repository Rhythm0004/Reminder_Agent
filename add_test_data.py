# add_test_data.py
from datetime import datetime, timedelta
from database import SessionLocal
from models import User, Medicine, Reminder

db = SessionLocal()

# Clean up old data if it exists
db.query(Reminder).delete()
db.query(User).delete()
db.query(Medicine).delete()

# Create User
user = User(name="Rhythm", email="rhythmai04@gmail.com")
db.add(user)
db.commit()
db.refresh(user)
print(f"Created user: {user.name}")

# Create Medicine with inventory that WILL trigger a refill alert
medicine = Medicine(name="Paracetamol", inventory=3, refill_threshold=5)
db.add(medicine)
db.commit()
db.refresh(medicine)
print(f"Created medicine: {medicine.name} (Inventory: {medicine.inventory})")

# Create a Reminder set to trigger in 1 minute
reminder_time = datetime.now() + timedelta(minutes=1)
reminder = Reminder(
    user_id=user.id,
    medicine_id=medicine.id,
    quantity=2,
    reminder_time=reminder_time,
    is_active=True
)
db.add(reminder)
db.commit()

print(f"Test reminder created. It will trigger at: {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}")
db.close()