# Mailing Management Service

## Overview
he Habit Reminder API is a Django REST Framework-based backend for managing personal habits. It allows users to create, track, and share habits with customizable settings like periodicity, duration, and rewards. The API supports authentication, ensuring users can manage their habits securely while also accessing public habits shared by others
## Installation and Setup

### 1. Clone the Repository

```bash
git clone git@github.com:RomanPecheritsa/HabitReminder.git
cd HabitReminder
```
### 2. Copy the env.example file to .env:
Open.env and replace the values of the variables with your own
```bash
cp .env.example .env
```
### 3. Install Dependencies
The project uses Poetry for dependency management. Ensure Poetry is installed, then run the following command to install all dependencies:
```bash
poetry shell
poetry install
```
### 4. Start Migrations
To start migrations, use the following command:
```bash
python3 manage.py migrate
```
### 5. Load Fixture
Loading test fixtures for the database:
```bash
python3 manage.py loaddata data.json
```

### 6. Run Server
To run server, use the following command:
```bash
python3 manage.py runserver
```
The server will be available at http://127.0.0.1:8000


### 7. Run Coverage Tests
To check the test coverage, use the following commands:
   ```bash
coverage run manage.py test
coverage report
   ```

### 8. Run Celery Worker
To start the Celery worker, use the following command:
```bash
celery -A habit_reminder worker --loglevel=info
```

### 9. Run Celery Beat
To start the Celery Beat scheduler, use the following command:
```bash
celery -A habit_reminder beat --loglevel=info
```


