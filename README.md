# Habit Reminder

## Overview
he Habit Reminder API is a Django REST Framework-based backend for managing personal habits. It allows users to create, track, and share habits with customizable settings like periodicity, duration, and rewards. The API supports authentication, ensuring users can manage their habits securely while also accessing public habits shared by others
## Installation and Setup with Docker

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
### 3. Build and Run Docker Containers
Execute the following command to build the Docker images:
```bash
docker-compose build
```
Start the application and its dependencies using:
```bash
docker-compose up
```

The server will be available at http://127.0.0.1:8000

### 4. Testing the Application
Run the tests with coverage: This command runs the Django tests and collects coverage data:
```bash
docker exec -it django coverage run --source='.' manage.py test
docker exec -it django coverage report
```

### 5. Stopping and Cleaning Up Docker Containers
To stop the running containers, use:
```bash
docker-compose down
```
If necessary, remove unused containers and images to free up space
```bash
docker system prune -a
```

### 6. Documentation
The full API documentation is available at: http://127.0.0.1:8000/swagger/




