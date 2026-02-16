# Quickstart: Chatbot Enhancements

## Setup

1.  **Prerequisites**: Make sure you have Python 3.11, Node.js 18+, and Docker installed.
2.  **Backend**:
    - Navigate to the `backend` directory.
    - Create a virtual environment: `python -m venv .venv`
    - Activate the virtual environment: `source .venv/bin/activate`
    - Install dependencies: `pip install -r requirements.txt`
    - Run the database migrations: `alembic upgrade head`
    - Start the backend server: `uvicorn app.main:app --reload`
3.  **Frontend**:
    - Navigate to the `frontend` directory.
    - Install dependencies: `npm install`
    - Start the frontend development server: `npm run dev`

## Running the Feature

1.  Open your web browser and navigate to `http://localhost:3000`.
2.  Log in with your user credentials.
3.  You should see the welcome message with your task statistics.
4.  Try creating a new task using the chatbot.
5.  Try creating a task with a similar title to an existing task to see the duplicate validation in action.
