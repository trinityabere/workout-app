# Workout Tracker API

A Flask + SQLAlchemy + Marshmallow backend for a workout tracking application
used by personal trainers. Trainers can build a reusable library of exercises
and attach them to workouts with sets/reps or a timed duration.

## Project Description

The API manages three related resources:

- **Exercise** — a reusable exercise (e.g. "Squat"), with a category and
  difficulty level. The same exercise can be attached to many workouts.
- **Workout** — a single training session with a date, duration, and notes.
- **WorkoutExercise** — the join between a workout and an exercise, storing
  the sets/reps or timed duration performed for that exercise in that
  specific workout.

A workout has many exercises through `WorkoutExercise`, and an exercise can
belong to many workouts through the same join table.

## Installation

1. Clone the repo and move into it:
```bash
   git clone https://github.com/trinityabere/workout-app.git
   cd workout-app
```
2. Create and activate a virtual environment, then install dependencies:
```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
```
3. Initialize and apply the database migrations:
```bash
   export FLASK_APP=app.py
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
```
4. Seed the database with example data:
```bash
   python seed.py
```

## Running the App

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5555`.

## Project Structure
