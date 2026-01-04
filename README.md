# Cura-Backend: Medicine Reminder Agent

This project is a Python-based backend service designed to function as a **Medicine Reminder Agent**. Its core purpose is to send timely notifications to users to take their medication and alert them when their medicine inventory is running low.

The agent is built with Flask and SQLAlchemy and is triggered via a simple API endpoint, making it easy to integrate with a scheduler like a cron job.

## Core Features

-   **API-Driven Trigger**: A simple `GET` endpoint to initiate the reminder-checking process.
-   **Email Notifications**: Sends personalized email reminders to users when it's time to take their medicine.
-   **Inventory Management**: Automatically decrements the medicine stock count after a reminder is sent.
-   **Refill Alerts**: Proactively sends a separate email alert if the medicine inventory falls below a user-defined threshold.
-   **Persistent Storage**: Uses a SQLite database to store user, medicine, and reminder information.
-   **Secure Configuration**: Manages sensitive credentials (like email passwords) securely using a `.env` file.

## Technology Stack

-   **Backend**: Python, Flask
-   **Database**: SQLite with SQLAlchemy (ORM)
-   **Configuration**: `python-dotenv` for environment variables

## Project Structure

```
cura-backend/
├── venv/
├── add_test_data.py   # Script to populate the DB with sample data
├── database.py        # Database engine and session setup
├── email_utils.py     # Handles sending emails via SMTP
├── init_db.py         # Script to create the database tables
├── main.py            # Main Flask application with the API endpoint
├── models.py          # SQLAlchemy ORM models (User, Medicine, Reminder)
├── new.env            # Environment variable template
└── reminder.db        # SQLite database file (created after init)
```

---

## Setup and Installation Guide

Follow these steps to get the Reminder Agent running on your local machine.

### Prerequisites

-   Python 3.7+
-   `pip` (Python package installer)

### 1. Clone the Repository

First, clone this repository to your local machine (or simply download the files into a new folder).

```bash
git clone <your-repository-url>
cd cura-backend
```

### 2. Set Up a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

Install all the required Python libraries using the `requirements.txt` file.

*First, create a file named `requirements.txt` with the following content:*

```txt
Flask
SQLAlchemy
python-dotenv
```

*Now, run the installation command:*
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

This project uses a `.env` file to handle your email credentials securely.

**Important:** You must use a **Google App Password**, not your regular Gmail password.
1.  Enable 2-Step Verification on your Google Account.
2.  Go to [Google App Passwords](https://myaccount.google.com/apppasswords) to generate a 16-character password for this application.

**Now, configure the project:**

1.  Rename the `new.env` file to `.env`.
2.  Open the `.env` file and replace the placeholder values with your credentials.

    ```env
    # .env
    EMAIL_USER=your-email@gmail.com
    EMAIL_PASS=your-16-character-app-password
    ```

---

## How to Run the Application

### 1. Initialize the Database

This command will create the `reminder.db` file and set up all the necessary tables.

```bash
python init_db.py
```

### 2. Add Test Data (Optional)

To test the system easily, you can run this script to add a sample user, a medicine, and a reminder scheduled for one minute in the future.

```bash
python add_test_data.py
```

### 3. Run the Flask Server

Start the application with this command. The server will run on `http://127.0.0.1:5000`.

```bash
python main.py
```

### 4. Trigger the Reminder Agent

Once the server is running, **wait for at least 60 seconds** (for the test reminder to become due), then open your web browser and navigate to the following URL:

```
http://127.0.0.1:5000/api/reminder/trigger/
```

-   **On the first run**, you should receive two emails (a reminder and a refill alert) and see a JSON response confirming the actions.
-   **On subsequent runs**, the agent will correctly report that 0 reminders were sent, as the initial one has been deactivated.

## API Endpoint

### `GET /api/reminder/trigger/`

This is the main endpoint that triggers the reminder agent's logic.

-   **Method**: `GET`
-   **Description**: Scans the database for all active reminders that are due. For each one, it sends the appropriate email notifications, updates the medicine inventory, and deactivates the reminder.
-   **Success Response (reminders sent)**:
    ```json
    {
      "status": "Reminder check completed.",
      "reminders_sent": 1,
      "refill_alerts": 1
    }
    ```

## Automation in Production

In a real-world scenario, you wouldn't trigger the agent manually from a browser. Instead, you would automate this process using a scheduler.

-   **Cron Job (Linux/macOS)**: A time-based job scheduler that can be configured to send a `curl` request to the API endpoint every minute.
    ```bash
    * * * * * curl http://your-production-url/api/reminder/trigger/
    ```
-   **Cloud Schedulers**: Services like GitHub Actions (on a schedule), AWS EventBridge, or Google Cloud Scheduler can be used to invoke the endpoint reliably.
