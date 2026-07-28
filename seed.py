from datetime import date

from server import create_app, db
from server.models import Exercise, Workout, WorkoutExercise

app = create_app()

with app.app_context():
    print("Clearing existing data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("Seeding exercises...")
    push_up = Exercise(name="Push Up", category="strength", difficulty="beginner")
    squat = Exercise(name="Squat", category="strength", difficulty="beginner")
    deadlift = Exercise(name="Deadlift", category="strength", equipment_needed="barbell, plates", difficulty="advanced")
    running = Exercise(name="Running", category="cardio", difficulty="intermediate")
    plank = Exercise(name="Plank", category="strength", difficulty="beginner")

    exercises = [push_up, squat, deadlift, running, plank]
    db.session.add_all(exercises)
    db.session.commit()

    print("Seeding workouts...")
    leg_day = Workout(date=date(2026, 7, 20), duration_minutes=45, notes="Leg day")
    full_body = Workout(date=date(2026, 7, 22), duration_minutes=60, notes="Full body circuit")
    cardio_day = Workout(date=date(2026, 7, 24), duration_minutes=30, notes="Easy cardio")

    workouts = [leg_day, full_body, cardio_day]
    db.session.add_all(workouts)
    db.session.commit()

    print("Linking exercises to workouts...")
    links = [
        WorkoutExercise(workout_id=leg_day.id, exercise_id=squat.id, sets=4, reps=10),
        WorkoutExercise(workout_id=leg_day.id, exercise_id=deadlift.id, sets=3, reps=8),
        WorkoutExercise(workout_id=full_body.id, exercise_id=push_up.id, sets=3, reps=15),
        WorkoutExercise(workout_id=full_body.id, exercise_id=squat.id, sets=3, reps=12),
        WorkoutExercise(workout_id=full_body.id, exercise_id=plank.id, duration_seconds=60),
        WorkoutExercise(workout_id=cardio_day.id, exercise_id=running.id, duration_seconds=1800),
    ]
    db.session.add_all(links)
    db.session.commit()

    print(f"Done! Seeded {len(exercises)} exercises, {len(workouts)} workouts, and {len(links)} links.")
