# main.py
from flask import Flask, jsonify
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Reminder, User, Medicine
from email_utils import send_email

app = Flask(__name__)

@app.route('/api/reminder/trigger/', methods=['GET'])
def trigger_reminder():
    db: Session = SessionLocal()
    now = datetime.now()
    
    # Find reminders that are due (past or present) and still active
    active_reminders = db.query(Reminder).filter(
        Reminder.is_active == True,
        Reminder.reminder_time <= now
    ).all()

    reminders_sent = 0
    refill_alerts = 0

    for reminder in active_reminders:
        user = reminder.user
        med = reminder.medicine

        try:
            # 1. Send the primary medicine reminder email
            subject = f"Time to take your medicine: {med.name}"
            message = f"Hi {user.name},\n\nIt's time to take {reminder.quantity} pill(s) of {med.name}.\n\nTake care!"
            send_email(user.email, subject, message)
            reminders_sent += 1

            # 2. Update medicine inventory in the database
            med.inventory -= reminder.quantity
            
            # 3. Deactivate the reminder so it doesn't trigger again
            reminder.is_active = False

            # 4. Check for low inventory and send a refill alert if needed
            if med.inventory <= med.refill_threshold:
                refill_subject = f"Refill Alert for {med.name}"
                refill_message = f"Hi {user.name},\n\nYour inventory for {med.name} is now at {med.inventory}.\nPlease refill it as soon as possible."
                send_email(user.email, refill_subject, refill_message)
                refill_alerts += 1
        
        except Exception as e:
            # If sending email fails, skip this reminder and go to the next one
            print(f"Skipping reminder for {user.name} due to an error.")
            continue
            
    # Commit all changes (inventory updates, deactivations) to the database
    db.commit()
    db.close()
    
    return jsonify({
        "status": "Reminder check completed.",
        "reminders_sent": reminders_sent,
        "refill_alerts": refill_alerts
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)